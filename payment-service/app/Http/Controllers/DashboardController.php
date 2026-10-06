<?php

namespace App\Http\Controllers;

use App\Models\Payment;
use App\Models\PaymentTransaction;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

class DashboardController extends Controller
{
    public function stats(): JsonResponse
    {
        $totalRevenue = Payment::where('status', 'paid')->sum('amount');
        $totalPaidOrders = Payment::where('status', 'paid')->count();
        $totalPendingOrders = Payment::where('status', 'pending')->count();
        $transactions = PaymentTransaction::latest()->limit(10)->get();

        return response()->json([
            'success' => true,
            'data' => [
                'total_revenue' => $totalRevenue,
                'total_orders' => $totalPaidOrders + $totalPendingOrders,
                'paid_orders' => $totalPaidOrders,
                'pending_orders' => $totalPendingOrders,
                'recent_transactions' => $transactions,
            ],
        ]);
    }

    public function financeReport(): JsonResponse
    {
        $transactions = PaymentTransaction::with('payment')->latest()->paginate(20);
        $totalMomo = PaymentTransaction::where('gateway', 'momo')->where('status', 'paid')->sum('amount');
        $totalCod = PaymentTransaction::where('gateway', 'cod')->where('status', 'paid')->sum('amount');

        return response()->json([
            'success' => true,
            'data' => [
                'transactions' => $transactions->items(),
                'pagination' => [
                    'current_page' => $transactions->currentPage(),
                    'total' => $transactions->total(),
                    'per_page' => $transactions->perPage(),
                ],
                'summary' => [
                    'momo_revenue' => $totalMomo,
                    'cod_revenue' => $totalCod,
                    'total_revenue' => $totalMomo + $totalCod,
                ],
            ],
        ]);
    }
}
