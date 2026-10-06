<?php

use App\Models\User;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Route;

Route::get('/', function () {
    $dbConnected = false;
    $dbName = '';
    $userCount = 0;
    $users = collect();
    $errorMessage = null;

    try {
        DB::connection()->getPdo();
        $dbConnected = true;
        $dbName = DB::connection()->getDatabaseName();
        $userCount = User::count();
        $users = User::latest()->take(10)->get();
    } catch (\Throwable $e) {
        $errorMessage = $e->getMessage();
    }

    return view('welcome', compact('dbConnected', 'dbName', 'userCount', 'users', 'errorMessage'));
});
