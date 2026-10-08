<?php

use App\Http\Controllers\AddressController;
use App\Http\Controllers\AuthController;
use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| Public Authentication Routes
|--------------------------------------------------------------------------
*/
$authRoutes = function (): void {
    Route::post('/register', [AuthController::class, 'register']);
    Route::post('/login', [AuthController::class, 'login']);
    Route::post('/forgot-password', [AuthController::class, 'forgotPassword']);
    Route::post('/forgot-password/send-otp', [AuthController::class, 'sendResetOtp']);
    Route::post('/forgot-password/verify-otp', [AuthController::class, 'verifyResetOtp']);
    Route::post('/verify-email', [AuthController::class, 'verifyEmail']);
    Route::post('/resend-otp', [AuthController::class, 'resendOtp']);
};

// Hỗ trợ cả 2 đường dẫn trực tiếp và có tiền tố /auth
$authRoutes();
Route::prefix('auth')->group($authRoutes);

/*
|--------------------------------------------------------------------------
| Protected Routes (Bearer Token via auth:api)
|--------------------------------------------------------------------------
*/
$protectedRoutes = function (): void {
    Route::get('/me', [AuthController::class, 'me']);
    Route::post('/logout', [AuthController::class, 'logout']);
    Route::match(['PUT', 'PATCH', 'POST'], '/profile', [AuthController::class, 'updateProfile']);

    // Address Management
    Route::get('/addresses', [AddressController::class, 'index']);
    Route::post('/addresses', [AddressController::class, 'store']);
    Route::match(['PUT', 'PATCH'], '/addresses/{address}', [AddressController::class, 'update']);
    Route::delete('/addresses/{address}', [AddressController::class, 'destroy']);
    Route::match(['PUT', 'PATCH', 'POST'], '/addresses/{address}/set-default', [AddressController::class, 'setDefault']);
    Route::match(['PUT', 'PATCH', 'POST'], '/addresses/{address}/default', [AddressController::class, 'setDefault']);

    // User Management (Protected Admin APIs)
    Route::get('/users', [AuthController::class, 'getUsers']);
    Route::patch('/users/{user}/status', [AuthController::class, 'updateUserStatus']);
};

Route::middleware('auth:api')->group($protectedRoutes);
Route::prefix('auth')->middleware('auth:api')->group($protectedRoutes);