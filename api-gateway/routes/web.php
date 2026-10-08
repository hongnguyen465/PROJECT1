<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Route;

Route::get('/', function () {
    return view('welcome');
});

Route::get('/payment/momo/callback', function (Request $request) {
    $paymentService = rtrim((string) config('services.microservices.payment', env('PAYMENT_SERVICE_URL', 'http://127.0.0.1:8004')), '/');
    try {
        Http::withoutVerifying()->timeout(5)->get("{$paymentService}/api/payment/momo/callback", $request->query());
    } catch (\Exception $e) {
        \Illuminate\Support\Facades\Log::error('Lỗi gọi callback payment-service từ web.php:', ['error' => $e->getMessage()]);
    }

    $status = (string) $request->input('resultCode', '0') === '0' ? 'success' : 'failed';
    $frontendUrl = rtrim((string) env('FRONTEND_URL', 'http://localhost:5173'), '/');
    $extraData = (string) $request->input('extraData', '');
    $transId = (string) $request->input('transId', '');

    return redirect("{$frontendUrl}/orders?status={$status}&order_code={$extraData}&transId={$transId}");
})->name('payment.momo.callback');

Route::post('/payment/momo/ipn', function (Request $request) {
    $paymentService = rtrim((string) config('services.microservices.payment', env('PAYMENT_SERVICE_URL', 'http://127.0.0.1:8004')), '/');
    try {
        $response = Http::withoutVerifying()->timeout(5)->post("{$paymentService}/api/payment/momo/ipn", $request->all());
        return response($response->body(), $response->status(), $response->headers());
    } catch (\Exception $e) {
        \Illuminate\Support\Facades\Log::error('Lỗi gọi IPN payment-service từ web.php:', ['error' => $e->getMessage()]);
        return response()->json(['message' => 'Internal Error'], 500);
    }
})->name('payment.momo.ipn');

// Proxy / Serve Chat Uploads from chat-service
Route::get('/uploads/chat/{filename}', function ($filename) {
    $localPath = base_path('../chat-service/public/uploads/chat/' . $filename);
    if (file_exists($localPath)) {
        return response()->file($localPath);
    }

    $chatService = rtrim((string) config('services.microservices.chat', env('CHAT_SERVICE_URL', 'http://127.0.0.1:8005')), '/');
    try {
        $response = Http::withoutVerifying()->timeout(5)->get("{$chatService}/uploads/chat/{$filename}");
        if ($response->successful()) {
            return response($response->body(), 200, [
                'Content-Type' => $response->header('Content-Type') ?: 'image/jpeg',
                'Cache-Control' => 'public, max-age=86400',
            ]);
        }
    } catch (\Exception $e) {
        \Illuminate\Support\Facades\Log::error('Lỗi proxy chat upload từ api-gateway:', ['error' => $e->getMessage()]);
    }

    return response()->json(['message' => 'File not found'], 404);
})->where('filename', '.*');

