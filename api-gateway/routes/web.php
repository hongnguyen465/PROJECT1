<?php
 
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Route;

Route::get('/', function () {
    return view('welcome');
});

Route::get('/payment/momo/callback', function (Request $request) {
    $paymentService = rtrim((string) config('services.microservices.payment', 'http://127.0.0.1:8004'), '/');
    try {
        Http::timeout(5)->get("{$paymentService}/api/payment/momo/callback", $request->query());
    } catch (\Exception $e) {
        \Illuminate\Support\Facades\Log::error('Lỗi gọi callback payment-service từ web.php:', ['error' => $e->getMessage()]);
    }
    $status = (string) $request->input('resultCode', '0') === '0' ? 'success' : 'failed';
    return redirect("http://localhost:5173/orders?status={$status}");
})->name('payment.momo.callback');

Route::post('/payment/momo/ipn', function (Request $request) {
    $paymentService = rtrim((string) config('services.microservices.payment', 'http://127.0.0.1:8004'), '/');
    try {
        $response = Http::timeout(5)->post("{$paymentService}/api/payment/momo/ipn", $request->all());
        return response($response->body(), $response->status(), $response->headers());
    } catch (\Exception $e) {
        \Illuminate\Support\Facades\Log::error('Lỗi gọi IPN payment-service từ web.php:', ['error' => $e->getMessage()]);
        return response()->json(['message' => 'Internal Error'], 500);
    }
})->name('payment.momo.ipn');


