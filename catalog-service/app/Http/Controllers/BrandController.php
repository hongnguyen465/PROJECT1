<?php

namespace App\Http\Controllers;

use App\Models\Brand;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Str;

class BrandController extends Controller
{
    public function index(): JsonResponse
    {
        $brands = Brand::withCount('products')->get();
        return response()->json([
            'success' => true,
            'data' => $brands,
        ]);
    }

    public function store(Request $request): JsonResponse
    {
        $validated = $request->validate([
            'name' => ['required', 'string', 'max:255'],
            'logo' => ['sometimes', 'nullable', 'string'],
            'logo_path' => ['sometimes', 'nullable', 'string'],
        ]);

        $validated['slug'] = Str::slug($validated['name']);
        $brand = Brand::create($validated);

        return response()->json([
            'success' => true,
            'message' => 'Tạo thương hiệu thành công',
            'data' => $brand,
        ], 201);
    }
}
