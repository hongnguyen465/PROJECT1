<?php

namespace App\Http\Controllers;

use App\Models\Banner;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

class BannerController extends Controller
{
    public function index(): JsonResponse
    {
        $banners = Banner::orderBy('order')->get();
        return response()->json([
            'success' => true,
            'data' => $banners,
        ]);
    }

    public function store(Request $request): JsonResponse
    {
        $validated = $request->validate([
            'title' => ['required', 'string', 'max:255'],
            'subtitle' => ['sometimes', 'nullable', 'string'],
            'tag' => ['sometimes', 'nullable', 'string'],
            'image' => ['required', 'string'],
            'link' => ['sometimes', 'nullable', 'string'],
            'order' => ['sometimes', 'integer'],
            'is_active' => ['sometimes', 'boolean'],
        ]);

        $banner = Banner::create($validated);

        return response()->json([
            'success' => true,
            'message' => 'Tạo banner thành công',
            'data' => $banner,
        ], 201);
    }

    public function update(Request $request, $id): JsonResponse
    {
        $banner = Banner::find($id);
        if (!$banner) {
            return response()->json(['success' => false, 'message' => 'Không tìm thấy banner'], 404);
        }

        $validated = $request->validate([
            'title' => ['sometimes', 'string', 'max:255'],
            'subtitle' => ['sometimes', 'nullable', 'string'],
            'tag' => ['sometimes', 'nullable', 'string'],
            'image' => ['sometimes', 'string'],
            'link' => ['sometimes', 'nullable', 'string'],
            'order' => ['sometimes', 'integer'],
            'is_active' => ['sometimes', 'boolean'],
        ]);

        $banner->update($validated);

        return response()->json([
            'success' => true,
            'message' => 'Cập nhật banner thành công',
            'data' => $banner->fresh(),
        ]);
    }

    public function destroy($id): JsonResponse
    {
        $banner = Banner::find($id);
        if (!$banner) {
            return response()->json(['success' => false, 'message' => 'Không tìm thấy banner'], 404);
        }

        $banner->delete();

        return response()->json([
            'success' => true,
            'message' => 'Xóa banner thành công',
        ]);
    }
}
