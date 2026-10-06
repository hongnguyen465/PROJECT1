<?php

use App\Http\Controllers\CartController;
use App\Http\Controllers\CouponController;
use App\Http\Controllers\OrderController;
use App\Http\Controllers\ReviewController;
use App\Http\Controllers\ShippingController;
use Illuminate\Support\Facades\Route;

// Orders routes
Route::prefix('orders')->group(function () {
    Route::get('/', [OrderController::class, 'index']);
    Route::post('/', [OrderController::class, 'store']);
    Route::get('/{id}', [OrderController::class, 'show']);
    Route::patch('/{id}/status', [OrderController::class, 'updateStatus']);
    Route::post('/{id}/ghn-ship', [OrderController::class, 'createGhnShipment']);
});

// Cart routes
Route::prefix('cart')->group(function () {
    Route::get('/', [CartController::class, 'index']);
    Route::post('/items', [CartController::class, 'addItem']);
    Route::patch('/items/{id}', [CartController::class, 'updateItem']);
    Route::delete('/items/{id}', [CartController::class, 'removeItem']);
    Route::delete('/clear', [CartController::class, 'clear']);
});

// Coupon routes
Route::prefix('coupons')->group(function () {
    Route::get('/', [CouponController::class, 'index']);
    Route::post('/', [CouponController::class, 'store']);
    Route::patch('/{id}', [CouponController::class, 'update']);
    Route::delete('/{id}', [CouponController::class, 'destroy']);
    Route::post('/apply', [CouponController::class, 'apply']);
});

// Shipping routes
Route::prefix('shipping')->group(function () {
    Route::get('/provinces', [ShippingController::class, 'getProvinces']);
    Route::get('/districts', [ShippingController::class, 'getDistricts']);
    Route::get('/wards', [ShippingController::class, 'getWards']);
    Route::post('/fee', [ShippingController::class, 'calculateFee']);
});

// Review routes
Route::prefix('reviews')->group(function () {
    Route::get('/', [ReviewController::class, 'index']);
    Route::get('/summary', [ReviewController::class, 'summary']);
    Route::post('/', [ReviewController::class, 'store']);
    Route::get('/check-reviewed', [ReviewController::class, 'checkReviewed']);
});
