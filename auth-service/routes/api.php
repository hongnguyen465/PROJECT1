<?php

use App\Http\Controllers\AddressController;
use App\Http\Controllers\Admin\ChatController as AdminChatController;
use App\Http\Controllers\AuthController;
use App\Http\Controllers\BannerController;
use App\Http\Controllers\BrandController;
use App\Http\Controllers\CartController;
use App\Http\Controllers\CategoryController;
use App\Http\Controllers\CouponController;
use App\Http\Controllers\DashboardController;
use App\Http\Controllers\MoMoPaymentController;
use App\Http\Controllers\OrderController;
use App\Http\Controllers\ProductController;
use App\Http\Controllers\ReviewController;
use App\Http\Controllers\ShippingController;
use App\Http\Controllers\UserChatController;
use Illuminate\Support\Facades\Route;

// ==================== AUTH & USERS ====================
Route::prefix('auth')->group(function () {
    Route::post('/register', [AuthController::class, 'register']);
    Route::post('/login', [AuthController::class, 'login']);
    Route::post('/verify-email', [AuthController::class, 'verifyEmail']);
    Route::post('/resend-otp', [AuthController::class, 'resendOtp']);
    Route::post('/forgot-password/send-otp', [AuthController::class, 'sendResetOtp']);
    Route::post('/forgot-password/verify-otp', [AuthController::class, 'verifyResetOtp']);
    Route::get('/me', [AuthController::class, 'me']);
    Route::post('/logout', [AuthController::class, 'logout']);
    Route::patch('/profile', [AuthController::class, 'updateProfile']);

    // Address routes
    Route::get('/addresses', [AddressController::class, 'index']);
    Route::post('/addresses', [AddressController::class, 'store']);
    Route::put('/addresses/{id}', [AddressController::class, 'update']);
    Route::delete('/addresses/{id}', [AddressController::class, 'destroy']);
    Route::patch('/addresses/{id}/default', [AddressController::class, 'setDefault']);
});

Route::get('/users', [AuthController::class, 'getUsers']);
Route::patch('/users/{user}/status', [AuthController::class, 'updateUserStatus']);

// ==================== CATALOG ====================
Route::prefix('products')->group(function () {
    Route::get('/', [ProductController::class, 'index']);
    Route::post('/', [ProductController::class, 'store']);
    Route::post('/check-stock', [ProductController::class, 'checkStock']);
    Route::get('/{id}', [ProductController::class, 'show']);
    Route::patch('/{id}', [ProductController::class, 'update']);
    Route::delete('/{id}', [ProductController::class, 'destroy']);
});

Route::prefix('categories')->group(function () {
    Route::get('/', [CategoryController::class, 'index']);
    Route::post('/', [CategoryController::class, 'store']);
});

Route::prefix('brands')->group(function () {
    Route::get('/', [BrandController::class, 'index']);
    Route::post('/', [BrandController::class, 'store']);
});

Route::prefix('banners')->group(function () {
    Route::get('/', [BannerController::class, 'index']);
    Route::post('/', [BannerController::class, 'store']);
    Route::patch('/{id}', [BannerController::class, 'update']);
    Route::delete('/{id}', [BannerController::class, 'destroy']);
});

// ==================== ORDERS & CART ====================
Route::prefix('cart')->group(function () {
    Route::get('/', [CartController::class, 'index']);
    Route::post('/', [CartController::class, 'store']);
    Route::patch('/items/{id}', [CartController::class, 'update']);
    Route::delete('/items/{id}', [CartController::class, 'destroy']);
    Route::delete('/clear', [CartController::class, 'clear']);
});

Route::prefix('orders')->group(function () {
    Route::get('/', [OrderController::class, 'index']);
    Route::post('/', [OrderController::class, 'store']);
    Route::get('/sales-summary', [OrderController::class, 'salesSummary']);
    Route::get('/{id}', [OrderController::class, 'show']);
    Route::patch('/{id}/status', [OrderController::class, 'updateStatus']);
    Route::post('/{id}/cancel', [OrderController::class, 'cancel']);
});

Route::prefix('coupons')->group(function () {
    Route::get('/', [CouponController::class, 'index']);
    Route::post('/apply', [CouponController::class, 'apply']);
    Route::post('/', [CouponController::class, 'store']);
    Route::patch('/{id}', [CouponController::class, 'update']);
    Route::delete('/{id}', [CouponController::class, 'destroy']);
});

Route::prefix('reviews')->group(function () {
    Route::get('/summary', [ReviewController::class, 'summary']);
    Route::get('/product/{productId}', [ReviewController::class, 'byProduct']);
    Route::post('/', [ReviewController::class, 'store']);
});

// ==================== SHIPPING ====================
Route::prefix('shipping')->group(function () {
    Route::get('/fee', [ShippingController::class, 'calculateFee']);
});

// ==================== PAYMENTS & FINANCE ====================
Route::prefix('payment')->group(function () {
    Route::post('/start', [MoMoPaymentController::class, 'start']);
    Route::post('/ipn', [MoMoPaymentController::class, 'ipn']);
    Route::get('/status/{orderId}', [MoMoPaymentController::class, 'status']);
});

Route::prefix('dashboard')->group(function () {
    Route::get('/stats', [DashboardController::class, 'stats']);
});

// ==================== CHAT ====================
Route::prefix('user/chat')->group(function () {
    Route::get('/messages', [UserChatController::class, 'getMessages']);
    Route::post('/send', [UserChatController::class, 'send']);
});

Route::prefix('admin/chat')->group(function () {
    Route::get('/users', [AdminChatController::class, 'getUsers']);
    Route::get('/messages/{userId}', [AdminChatController::class, 'getMessages']);
    Route::post('/send', [AdminChatController::class, 'send']);
    Route::get('/unread-count', [AdminChatController::class, 'getUnreadCount']);
    Route::get('/search-customers', [AdminChatController::class, 'searchCustomers']);
    Route::get('/user-detail/{userId}', [AdminChatController::class, 'getUserDetail']);
    Route::post('/mark-as-read/{userId}', [AdminChatController::class, 'markAsRead']);
});
