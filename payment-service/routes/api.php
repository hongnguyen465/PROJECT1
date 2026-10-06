<?php

use App\Http\Controllers\DashboardController;
use App\Http\Controllers\MoMoPaymentController;
use Illuminate\Support\Facades\Route;

// Payment routes
Route::prefix('payment')->group(function () {
    Route::post('/momo/start', [MoMoPaymentController::class, 'start']);
    Route::post('/momo/create', [MoMoPaymentController::class, 'start']);
    Route::post('/momo/ipn', [MoMoPaymentController::class, 'ipn']);
});

Route::get('/payments/status', [MoMoPaymentController::class, 'status']);

// Dashboard & Finance routes (Lab 9)
Route::get('/dashboard/stats', [DashboardController::class, 'stats']);
Route::get('/finance/transactions', [DashboardController::class, 'financeReport']);
Route::get('/finance/report', [DashboardController::class, 'financeReport']);
