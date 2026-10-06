<?php

namespace App\Http\Controllers;

use App\Models\Product;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Str;

class ProductController extends Controller
{
    public function index(Request $request): JsonResponse
    {
        $search = $request->input('search');
        $category = $request->input('category');
        $brand = $request->input('brand');
        $tag = $request->input('tag');
        $sort = $request->input('sort', 'latest');
        $perPage = (int) $request->input('per_page', 50);

        $query = Product::with(['category', 'brand', 'variants', 'productImages'])
            ->when($search, function ($q, $s) {
                $q->where(function ($sub) use ($s) {
                    $sub->where('name', 'like', "%{$s}%")
                        ->orWhere('sku', 'like', "%{$s}%")
                        ->orWhere('description', 'like', "%{$s}%");
                });
            })
            ->when($category, function ($q, $c) {
                if (is_numeric($c)) {
                    $q->where('category_id', $c);
                } else {
                    $q->whereHas('category', fn($sub) => $sub->where('slug', $c));
                }
            })
            ->when($brand, function ($q, $b) {
                if (is_numeric($b)) {
                    $q->where('brand_id', $b);
                } else {
                    $q->whereHas('brand', fn($sub) => $sub->where('slug', $b));
                }
            })
            ->when($tag, fn($q, $t) => $q->where('tag', $t));

        switch ($sort) {
            case 'price_asc':
                $query->orderBy('price', 'asc');
                break;
            case 'price_desc':
                $query->orderBy('price', 'desc');
                break;
            case 'name_asc':
                $query->orderBy('name', 'asc');
                break;
            default:
                $query->latest();
                break;
        }

        $products = $query->paginate($perPage);

        return response()->json([
            'success' => true,
            'data' => $products->items(),
            'pagination' => [
                'current_page' => $products->currentPage(),
                'per_page' => $products->perPage(),
                'total' => $products->total(),
                'last_page' => $products->lastPage(),
            ],
        ]);
    }

    public function show($id): JsonResponse
    {
        $product = Product::with(['category', 'brand', 'variants', 'productImages'])->find($id);
        if (!$product) {
            return response()->json(['success' => false, 'message' => 'Không tìm thấy sản phẩm'], 404);
        }

        return response()->json([
            'success' => true,
            'data' => $product,
        ]);
    }

    public function store(Request $request): JsonResponse
    {
        $validated = $request->validate([
            'name' => ['required', 'string', 'max:255'],
            'category_id' => ['sometimes', 'nullable', 'integer'],
            'brand_id' => ['sometimes', 'nullable', 'integer'],
            'price' => ['required', 'numeric', 'min:0'],
            'old_price' => ['sometimes', 'nullable', 'numeric'],
            'tag' => ['sometimes', 'nullable', 'string'],
            'stock' => ['sometimes', 'integer', 'min:0'],
            'sku' => ['sometimes', 'nullable', 'string'],
            'image_url' => ['sometimes', 'nullable', 'string'],
            'images' => ['sometimes', 'nullable', 'array'],
            'colors' => ['sometimes', 'nullable', 'array'],
            'sizes' => ['sometimes', 'nullable', 'array'],
            'description' => ['sometimes', 'nullable', 'string'],
        ]);

        $validated['slug'] = Str::slug($validated['name']) . '-' . Str::random(5);
        if (empty($validated['sku'])) {
            $validated['sku'] = 'STR-' . strtoupper(Str::random(6));
        }

        $product = Product::create($validated);

        return response()->json([
            'success' => true,
            'message' => 'Tạo sản phẩm thành công',
            'data' => $product,
        ], 201);
    }

    public function update(Request $request, $id): JsonResponse
    {
        $product = Product::find($id);
        if (!$product) {
            return response()->json(['success' => false, 'message' => 'Không tìm thấy sản phẩm'], 404);
        }

        $validated = $request->validate([
            'name' => ['sometimes', 'string', 'max:255'],
            'category_id' => ['sometimes', 'nullable', 'integer'],
            'brand_id' => ['sometimes', 'nullable', 'integer'],
            'price' => ['sometimes', 'numeric', 'min:0'],
            'old_price' => ['sometimes', 'nullable', 'numeric'],
            'tag' => ['sometimes', 'nullable', 'string'],
            'stock' => ['sometimes', 'integer', 'min:0'],
            'sku' => ['sometimes', 'nullable', 'string'],
            'image_url' => ['sometimes', 'nullable', 'string'],
            'images' => ['sometimes', 'nullable', 'array'],
            'colors' => ['sometimes', 'nullable', 'array'],
            'sizes' => ['sometimes', 'nullable', 'array'],
            'description' => ['sometimes', 'nullable', 'string'],
            'is_active' => ['sometimes', 'boolean'],
        ]);

        $product->update($validated);

        return response()->json([
            'success' => true,
            'message' => 'Cập nhật sản phẩm thành công',
            'data' => $product->fresh(['category', 'brand', 'variants', 'productImages']),
        ]);
    }

    public function destroy($id): JsonResponse
    {
        $product = Product::find($id);
        if (!$product) {
            return response()->json(['success' => false, 'message' => 'Không tìm thấy sản phẩm'], 404);
        }

        $product->delete();

        return response()->json([
            'success' => true,
            'message' => 'Xóa sản phẩm thành công',
        ]);
    }

    public function checkStock(Request $request): JsonResponse
    {
        $items = $request->input('items', []);
        $results = [];

        foreach ($items as $item) {
            $productId = $item['product_id'] ?? 0;
            $qty = $item['quantity'] ?? 1;
            $product = Product::find($productId);

            $available = $product ? ($product->stock >= $qty) : false;
            $results[] = [
                'product_id' => $productId,
                'requested' => $qty,
                'in_stock' => $product ? $product->stock : 0,
                'available' => $available,
            ];
        }

        return response()->json([
            'success' => true,
            'data' => $results,
        ]);
    }
}
