<?php

use App\Http\Controllers\GatewayController;
use Illuminate\Support\Facades\Route;

// Catch all API requests and forward through GatewayController
Route::any('/{path?}', [GatewayController::class, 'handle'])->where('path', '.*');
