<?php

namespace App\Http\Controllers;

use App\Models\Payment;
use App\Models\PaymentTransaction;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Str;

class MoMoPaymentController extends Controller
{
    public function start(Request $request): JsonResponse
    {
        $orderId = (int) $request->input('order_id');
        $amount = (float) ($request->input('amount') ?? 50000);

        if (!$orderId) {
            return response()->json(['success' => false, 'message' => 'Order ID is required'], 400);
        }

        $payment = Payment::updateOrCreate(
            ['order_id' => $orderId],
            [
                'payment_method' => 'momo',
                'amount' => $amount,
                'status' => 'pending',
            ]
        );

        $transactionCode = 'MOMO_' . time() . '_' . Str::random(6);

        $transaction = PaymentTransaction::create([
            'payment_id' => $payment->id,
            'gateway' => 'momo',
            'transaction_code' => $transactionCode,
            'amount' => $amount,
            'status' => 'pending',
            'raw_payload' => $request->all(),
        ]);

        // Demo redirect URL for MoMo callback in Sandbox / Dev
        $payUrl = "http://localhost:5173/payment/callback?partnerCode=MOMO&orderId={$orderId}&amount={$amount}&resultCode=0&message=Successful";

        return response()->json([
            'success' => true,
            'message' => 'Tạo liên kết thanh toán MoMo thành công',
            'data' => [
                'pay_url' => $payUrl,
                'order_id' => $orderId,
                'payment_id' => $payment->id,
                'transaction_id' => $transaction->id,
                'transaction_code' => $transactionCode,
            ],
            'pay_url' => $payUrl,
        ]);
    }

    public function status(Request $request): JsonResponse
    {
        $orderId = (int) $request->input('order_id');
        $payment = Payment::where('order_id', $orderId)->first();

        if (!$payment) {
            return response()->json([
                'success' => true,
                'data' => [
                    'order_id' => $orderId,
                    'status' => 'pending',
                ],
            ]);
        }

        return response()->json([
            'success' => true,
            'data' => [
                'order_id' => $orderId,
                'status' => $payment->status,
                'payment_method' => $payment->payment_method,
                'amount' => $payment->amount,
                'paid_at' => $payment->paid_at,
            ],
        ]);
    }

    public function ipn(Request $request): JsonResponse
    {
        $orderId = (int) $request->input('orderId');
        $resultCode = (int) $request->input('resultCode', 0);

        $payment = Payment::where('order_id', $orderId)->first();
        if ($payment) {
            $status = ($resultCode === 0) ? 'paid' : 'failed';
            $payment->update([
                'status' => $status,
                'paid_at' => ($status === 'paid') ? now() : null,
            ]);

            PaymentTransaction::create([
                'payment_id' => $payment->id,
                'gateway' => 'momo',
                'transaction_code' => $request->input('transId') ?? ('MOMO_IPN_' . time()),
                'response_code' => (string) $resultCode,
                'amount' => (float) $request->input('amount', $payment->amount),
                'status' => $status,
                'raw_payload' => $request->all(),
            ]);
        }

        return response()->json(['success' => true, 'message' => 'IPN processed']);
    }
}
