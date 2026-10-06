<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Http\Response;
use Illuminate\Support\Facades\Http;

class GatewayController extends Controller
{
    /**
     * Map microservice port based on prefix
     */
    protected function getServiceUrl(string $path): string
    {
        $segments = explode('/', ltrim($path, '/'));
        $prefix = strtolower($segments[0] ?? '');

        // Service mappings
        $ports = [
            // Auth service (8001)
            'auth' => 8001,
            'users' => 8001,
            'user' => 8001,
            'admin' => 8001,

            // Catalog service (8002)
            'products' => 8002,
            'categories' => 8002,
            'brands' => 8002,
            'banners' => 8002,

            // Order service (8003)
            'orders' => 8003,
            'cart' => 8003,
            'coupons' => 8003,
            'shipping' => 8003,
            'reviews' => 8003,

            // Payment service (8004)
            'payment' => 8004,
            'payments' => 8004,
            'finance' => 8004,
            'dashboard' => 8004,
        ];

        // Specific sub-route overrides
        if ($prefix === 'admin' && isset($segments[1]) && $segments[1] !== 'chat') {
            // e.g. admin/orders -> 8003, admin/products -> 8002, admin/finance -> 8004
            $sub = strtolower($segments[1]);
            if (in_array($sub, ['products', 'categories', 'brands', 'banners'])) {
                $port = 8002;
            } elseif (in_array($sub, ['orders', 'coupons'])) {
                $port = 8003;
            } elseif (in_array($sub, ['finance', 'dashboard', 'payments'])) {
                $port = 8004;
            } else {
                $port = 8001;
            }
            return "http://127.0.0.1:{$port}/api/{$path}";
        }

        $port = $ports[$prefix] ?? 8001;
        return "http://127.0.0.1:{$port}/api/{$path}";
    }

    /**
     * Reverse Proxy Handler
     */
    public function handle(Request $request, string $path = '')
    {
        $targetUrl = $this->getServiceUrl($path);
        $method = strtolower($request->method());

        // Forward headers (strip host)
        $headers = collect($request->header())
            ->map(fn($v) => is_array($v) ? implode(', ', $v) : $v)
            ->except(['host', 'content-length'])
            ->toArray();

        // Prepare HTTP client
        $client = Http::withHeaders($headers)
            ->timeout(15)
            ->withoutRedirecting();

        // Handle multipart / file uploads if any
        if ($request->hasFile('*')) {
            foreach ($request->allFiles() as $key => $file) {
                if (is_array($file)) {
                    foreach ($file as $f) {
                        $client = $client->attach($key . '[]', fopen($f->getRealPath(), 'r'), $f->getClientOriginalName());
                    }
                } else {
                    $client = $client->attach($key, fopen($file->getRealPath(), 'r'), $file->getClientOriginalName());
                }
            }
        }

        $queryParams = $request->query();
        $body = $request->isJson() ? $request->json()->all() : $request->all();

        try {
            if ($method === 'get' || $method === 'head') {
                $response = $client->get($targetUrl, $queryParams);
            } elseif ($method === 'post') {
                $response = $client->withQueryParameters($queryParams)->post($targetUrl, $body);
            } elseif ($method === 'put') {
                $response = $client->withQueryParameters($queryParams)->put($targetUrl, $body);
            } elseif ($method === 'patch') {
                $response = $client->withQueryParameters($queryParams)->patch($targetUrl, $body);
            } elseif ($method === 'delete') {
                $response = $client->withQueryParameters($queryParams)->delete($targetUrl, $body);
            } else {
                $response = $client->withQueryParameters($queryParams)->send($method, $targetUrl, ['json' => $body]);
            }

            return response($response->body(), $response->status())
                ->header('Content-Type', $response->header('Content-Type') ?? 'application/json');
        } catch (\Exception $e) {
            return response()->json([
                'success' => false,
                'message' => 'Lỗi kết nối tới dịch vụ nội bộ: ' . $e->getMessage(),
                'target' => $targetUrl,
            ], 503);
        }
    }
}
