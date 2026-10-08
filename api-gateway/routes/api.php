<?php

use App\Http\Controllers\GatewayController;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Route;

// MoMo Browser Callback Redirect Handler
Route::get('/payment/momo/callback', function (Illuminate\Http\Request $request) {
    $paymentService = rtrim((string) config('services.microservices.payment', 'http://127.0.0.1:8004'), '/');

    // 1. Gửi callback sang Payment Service (Port 8004) để xác thực chữ ký HMAC và đồng bộ đơn hàng
    try {
        Http::get("{$paymentService}/api/payment/momo/callback", $request->query());
    } catch (\Exception $e) {
        \Illuminate\Support\Facades\Log::error('Lỗi gọi callback payment-service từ api-gateway:', ['error' => $e->getMessage()]);
    }

    $status = (string) $request->input('resultCode', '0') === '0' ? 'success' : 'failed';
    // 2. Chuyển hướng trình duyệt về trang kết quả đơn hàng Frontend React
    return redirect("/orders?status={$status}");
});

// MoMo Server Webhook IPN Handler
Route::post('/payment/momo/ipn', function (Illuminate\Http\Request $request) {
    $paymentService = rtrim((string) config('services.microservices.payment', 'http://127.0.0.1:8004'), '/');
    try {
        $response = Http::post("{$paymentService}/api/payment/momo/ipn", $request->all());
        return response($response->body(), $response->status(), $response->headers());
    } catch (\Exception $e) {
        \Illuminate\Support\Facades\Log::error('Lỗi gọi IPN payment-service từ api-gateway:', ['error' => $e->getMessage()]);
        return response()->json(['message' => 'Internal Error'], 500);
    }
});

// Auth Service Routes
Route::any('/auth/{any?}', [GatewayController::class, 'auth'])->where('any', '.*');
Route::any('/addresses/{any?}', [GatewayController::class, 'auth'])->where('any', '.*');
Route::any('/users/{any?}', [GatewayController::class, 'auth'])->where('any', '.*');

// Chat Service Routes (Dedicated Chatbox Microservice + Gemini AI)
Route::any('/chat/{any?}', [GatewayController::class, 'chat'])->where('any', '.*');
Route::any('/user/chat/{any?}', [GatewayController::class, 'chat'])->where('any', '.*');
Route::any('/admin/chat/{any?}', [GatewayController::class, 'chat'])->where('any', '.*');

// Chặn truy cập công khai vào endpoint nội bộ của Catalog Service (SEC-02)
Route::match(['POST', 'PUT', 'PATCH', 'DELETE'], '/products/deduct-stock', function () {
    return response()->json([
        'success' => false,
        'error' => [
            'code' => 'FORBIDDEN',
            'message' => 'Endpoint nội bộ chỉ dành cho giao tiếp giữa các microservices.',
        ],
    ], 403);
});

Route::match(['POST', 'PUT', 'PATCH', 'DELETE'], '/products/restore-stock', function () {
    return response()->json([
        'success' => false,
        'error' => [
            'code' => 'FORBIDDEN',
            'message' => 'Endpoint nội bộ chỉ dành cho giao tiếp giữa các microservices.',
        ],
    ], 403);
});

// Catalog Service Routes
Route::any('/categories/{any?}', [GatewayController::class, 'catalog'])->where('any', '.*');
Route::any('/products/{any?}', [GatewayController::class, 'catalog'])->where('any', '.*');
Route::any('/brands/{any?}', [GatewayController::class, 'catalog'])->where('any', '.*');
Route::any('/banners/{any?}', [GatewayController::class, 'catalog'])->where('any', '.*');

// Order Service Routes
Route::any('/cart/{any?}', [GatewayController::class, 'order'])->where('any', '.*');
Route::any('/orders/{any?}', [GatewayController::class, 'order'])->where('any', '.*');
Route::any('/coupons/{any?}', [GatewayController::class, 'order'])->where('any', '.*');
Route::any('/reviews/{any?}', [GatewayController::class, 'order'])->where('any', '.*');
Route::any('/shipping/{any?}', [GatewayController::class, 'order'])->where('any', '.*');

// Payment Service Routes (Port 8004)
Route::any('/payments/{any?}', [GatewayController::class, 'payment'])->where('any', '.*');
Route::any('/payment/{any?}', [GatewayController::class, 'payment'])->where('any', '.*');

// Chat Uploads via /api/uploads/chat/{filename}
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

