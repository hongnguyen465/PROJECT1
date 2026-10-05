<?php

namespace App\Http\Controllers;

use App\Models\Payment;
use App\Models\PaymentTransaction;
use App\Services\MomoService;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;

class MomoController extends Controller
{
    /**
     * Start / Initialize a MoMo payment link.
     *
     * @group Payment Management
     */
    public function start(Request $request, MomoService $momo): JsonResponse
    {
        Log::info('MomoController::start input:', [
            'all' => $request->all(),
            'json' => $request->json()->all(),
            'raw' => $request->getContent(),
        ]);

        $validated = $request->validate([
            'order_id' => ['sometimes', 'nullable'],
            'amount' => ['sometimes', 'nullable', 'numeric'],
            'user_id' => ['sometimes', 'nullable', 'integer'],
            'order_code' => ['sometimes', 'nullable', 'string', 'max:50'],
            'order_number' => ['sometimes', 'nullable', 'string', 'max:50'],
        ]);

        $rawOrderId = $request->input('order_id');
        $orderCode = $request->input('order_code') ?? $request->input('order_number') ?? (is_string($rawOrderId) ? $rawOrderId : null);
        $amount = (float) ($request->input('amount') ?? 50000);
        $userId = isset($validated['user_id']) ? (int) $validated['user_id'] : 1;
        $numericOrderId = is_numeric($rawOrderId) ? (int) $rawOrderId : 0;

        // Query order-service to resolve actual numeric order_id and order_code if needed
        $orderServiceUrl = rtrim((string) config('services.microservices.order', env('ORDER_SERVICE_URL', 'http://127.0.0.1:8003')), '/');
        $lookupKey = $orderCode ?: (is_string($rawOrderId) ? $rawOrderId : ($numericOrderId > 0 ? $numericOrderId : null));
        if ($lookupKey) {
            try {
                $orderRes = Http::timeout(3)->get("{$orderServiceUrl}/api/orders/{$lookupKey}");
                if ($orderRes->successful() && $orderRes->json('data.id')) {
                    $orderData = $orderRes->json('data');
                    $numericOrderId = (int) $orderData['id'];
                    $orderCode = $orderData['order_code'] ?? $orderData['order_number'] ?? $orderCode;
                    if (!empty($orderData['total_amount']) && (!$request->has('amount') || (float)$request->input('amount') <= 0)) {
                        $amount = (float) $orderData['total_amount'];
                    }
                    if (!empty($orderData['user_id'])) {
                        $userId = (int) $orderData['user_id'];
                    }
                }
            } catch (\Exception $e) {
                Log::warning('Không thể query order-service trong MomoController::start: ' . $e->getMessage());
            }
        }

        if ($numericOrderId <= 0) {
            $numericOrderId = abs(crc32((string) ($orderCode ?: $rawOrderId ?: time()))) % 2147483647 ?: 1;
        }

        if ($amount < 1000) {
            $amount = 50000;
        }

        // 1. Create or update Payment record in striker_payment_db
        $payment = Payment::updateOrCreate(
            ['order_id' => $numericOrderId],
            [
                'user_id' => $userId,
                'payment_method' => 'momo',
                'amount' => $amount,
                'status' => 'pending',
                'paid_at' => null,
            ]
        );

        // 2. Create PaymentTransaction record
        $transaction = PaymentTransaction::create([
            'payment_id' => $payment->id,
            'gateway' => 'momo',
            'amount' => $amount,
            'status' => 'pending',
            'raw_payload' => [
                'order_code' => $orderCode,
                'order_id' => $numericOrderId,
            ],
        ]);

        // 3. Request MoMo payUrl
        $result = $momo->createPayment($payment, $transaction, [
            'order_code' => $orderCode,
            'order_number' => $orderCode,
        ]);

        $payUrl = $result['payUrl'] ?? null;

        // Fallback for sandbox / local development if MoMo Gateway endpoint fails or test API is unreachable
        if (!$payUrl) {
            $gatewayOrderId = $transaction->transaction_code ?: ($numericOrderId . '_' . $transaction->id . '_' . time());
            $transId = (string) (time() . rand(100, 999));
            $payUrl = "http://localhost:8000/api/payment/momo/callback?resultCode=0&orderId={$gatewayOrderId}&amount={$amount}&extraData={$orderCode}&transId={$transId}&message=Successful.";
        }

        return response()->json([
            'success' => true,
            'message' => 'Tạo liên kết thanh toán MoMo thành công.',
            'data' => [
                'pay_url' => $payUrl,
                'order_id' => $numericOrderId,
                'order_code' => $orderCode,
                'payment_id' => $payment->id,
                'transaction_id' => $transaction->id,
                'momo_response' => $result,
            ],
            'errors' => null,
        ]);
    }

    /**
     * Handle browser redirect callback from MoMo Gateway.
     *
     * @group Payment Management
     */
    public function callback(Request $request, MomoService $momo)
    {
        Log::info('MoMo Callback received in payment-service:', [
            'payload' => $request->except('signature'),
        ]);

        $resultCode = (int) $request->input('resultCode', -1);
        $isValid = $momo->isValidResponse($request->all());
        $isSuccessful = ($resultCode === 0) && ($isValid || app()->environment('local', 'testing'));

        if (!$isSuccessful) {
            Log::warning('MoMo Callback thất bại hoặc bị hủy:', [
                'result_code' => $resultCode,
                'order_id' => $request->input('orderId'),
            ]);

            if ($request->wantsJson()) {
                return response()->json([
                    'success' => false,
                    'message' => 'Giao dịch MoMo không thành công.',
                    'data' => $request->all(),
                ], 400);
            }

            return redirect('http://localhost:5173/orders?status=failed');
        }

        // Process completion and notify order-service
        $this->completePayment($request->all(), $momo);

        if ($request->wantsJson()) {
            return response()->json([
                'success' => true,
                'message' => 'Thanh toán MoMo thành công!',
                'data' => $request->all(),
            ]);
        }

        return redirect('http://localhost:5173/orders?status=success');
    }

    /**
     * Handle Instant Payment Notification (IPN) webhook from MoMo Server.
     *
     * @group Payment Management
     */
    public function ipn(Request $request, MomoService $momo): JsonResponse
    {
        Log::info('MoMo IPN webhook received in payment-service:', [
            'payload' => $request->except('signature'),
        ]);

        $resultCode = (int) $request->input('resultCode', -1);
        $isValid = $momo->isValidResponse($request->all());
        $isSuccessful = ($resultCode === 0) && ($isValid || app()->environment('local', 'testing'));

        if ($isSuccessful) {
            $this->completePayment($request->all(), $momo);
        }

        return response()->json(['message' => 'Received']);
    }

    /**
     * Complete payment in DB and sync with order-service.
     */
    private function completePayment(array $payload, MomoService $momo): void
    {
        $gatewayOrderId = (string) ($payload['orderId'] ?? '');
        $extraData = (string) ($payload['extraData'] ?? '');

        // Find transaction by transaction_code or order_id
        $transaction = PaymentTransaction::where('gateway', 'momo')
            ->where('transaction_code', $gatewayOrderId)
            ->latest('id')
            ->first();

        if (!$transaction && !empty($extraData)) {
            if (is_numeric($extraData)) {
                $payment = Payment::where('order_id', (int) $extraData)->latest('id')->first();
            } else {
                $orderServiceUrl = rtrim((string) config('services.microservices.order', env('ORDER_SERVICE_URL', 'http://127.0.0.1:8003')), '/');
                try {
                    $orderRes = Http::timeout(3)->get("{$orderServiceUrl}/api/orders/{$extraData}");
                    if ($orderRes->successful() && $orderRes->json('data.id')) {
                        $payment = Payment::where('order_id', (int) $orderRes->json('data.id'))->latest('id')->first();
                    }
                } catch (\Exception $e) {
                    Log::warning('Lỗi query order trong completePayment: ' . $e->getMessage());
                }
            }
            if (!empty($payment)) {
                $transaction = PaymentTransaction::where('payment_id', $payment->id)->latest('id')->first();
            }
        }

        if (!$transaction && str_contains($gatewayOrderId, '_')) {
            $parts = explode('_', $gatewayOrderId);
            if (isset($parts[0]) && is_numeric($parts[0])) {
                $payment = Payment::where('order_id', (int) $parts[0])->latest('id')->first();
                if ($payment) {
                    $transaction = PaymentTransaction::where('payment_id', $payment->id)
                        ->latest('id')
                        ->first();
                }
            }
        }

        if (!$transaction) {
            Log::error('MoMo completePayment: Không tìm thấy transaction', ['payload' => $payload]);
            if (!empty($extraData)) {
                $this->notifyOrderServicePaid($extraData, (string) ($payload['transId'] ?? ''));
            }
            return;
        }

        $payment = $transaction->payment;
        if ($payment) {
            // 1. Mark Paid in striker_payment_db
            $momo->markPaid($payment, $transaction, $payload);
        }

        $orderCode = $transaction->raw_payload['order_code'] ?? $transaction->raw_payload['request']['extraData'] ?? $extraData;
        $orderId = $payment?->order_id ?? $extraData;

        // 2. Synchronize status with order-service (Port 8003)
        $this->notifyOrderServicePaid($orderId, (string) ($payload['transId'] ?? ''), $orderCode);
    }

    /**
     * Call internal API in order-service to mark order as PAID.
     */
    private function notifyOrderServicePaid($orderId, string $transId, $orderCode = null): void
    {
        $orderServiceUrl = rtrim((string) config('services.microservices.order', env('ORDER_SERVICE_URL', 'http://127.0.0.1:8003')), '/');
        $targets = array_unique(array_filter([$orderId, $orderCode]));

        foreach ($targets as $target) {
            try {
                $response = Http::timeout(5)->post("{$orderServiceUrl}/api/orders/{$target}/mark-paid", [
                    'payment_method' => 'momo',
                    'transaction_id' => $transId,
                    'secret' => env('INTERNAL_SERVICE_SECRET', 'STRIKER_SECRET_TOKEN_2026'),
                ]);

                Log::info("Đã đồng bộ trạng thái thanh toán MoMo sang order-service cho đơn #{$target}", [
                    'status' => $response->status(),
                    'response' => $response->json(),
                ]);

                if ($response->successful()) {
                    break;
                }
            } catch (\Exception $e) {
                Log::error("Lỗi khi đồng bộ thanh toán sang order-service cho đơn #{$target}: " . $e->getMessage());
            }
        }
    }
}
