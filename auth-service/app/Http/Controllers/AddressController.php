<?php

namespace App\Http\Controllers;

use App\Models\Address;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

class AddressController extends Controller
{
    public function index(Request $request): JsonResponse
    {
        $userId = $request->input('user_id') ?? auth('api')->id();
        if (!$userId) {
            return response()->json(['success' => false, 'message' => 'User ID is required', 'data' => []], 400);
        }

        $addresses = Address::where('user_id', $userId)
            ->orderByDesc('is_default')
            ->orderByDesc('id')
            ->get();

        return response()->json([
            'success' => true,
            'data' => $addresses,
        ]);
    }

    public function store(Request $request): JsonResponse
    {
        $userId = $request->input('user_id') ?? auth('api')->id();
        if (!$userId) {
            return response()->json(['success' => false, 'message' => 'User ID is required'], 400);
        }

        $validated = $request->validate([
            'recipient_name' => ['required', 'string', 'max:255'],
            'phone' => ['required', 'string', 'max:20'],
            'province' => ['required', 'string', 'max:255'],
            'district' => ['required', 'string', 'max:255'],
            'ward' => ['required', 'string', 'max:255'],
            'street_address' => ['required', 'string', 'max:255'],
            'is_default' => ['sometimes', 'boolean'],
        ]);

        $isDefault = !empty($validated['is_default']);

        // If this is first address or marked default
        $count = Address::where('user_id', $userId)->count();
        if ($count === 0) {
            $isDefault = true;
        } elseif ($isDefault) {
            Address::where('user_id', $userId)->update(['is_default' => false]);
        }

        $address = Address::create([
            'user_id' => $userId,
            'recipient_name' => $validated['recipient_name'],
            'phone' => $validated['phone'],
            'province' => $validated['province'],
            'district' => $validated['district'],
            'ward' => $validated['ward'],
            'street_address' => $validated['street_address'],
            'is_default' => $isDefault,
        ]);

        return response()->json([
            'success' => true,
            'message' => 'Thêm địa chỉ thành công',
            'data' => $address,
        ], 201);
    }

    public function update(Request $request, int $id): JsonResponse
    {
        $address = Address::find($id);
        if (!$address) {
            return response()->json(['success' => false, 'message' => 'Không tìm thấy địa chỉ'], 404);
        }

        $validated = $request->validate([
            'recipient_name' => ['sometimes', 'string', 'max:255'],
            'phone' => ['sometimes', 'string', 'max:20'],
            'province' => ['sometimes', 'string', 'max:255'],
            'district' => ['sometimes', 'string', 'max:255'],
            'ward' => ['sometimes', 'string', 'max:255'],
            'street_address' => ['sometimes', 'string', 'max:255'],
            'is_default' => ['sometimes', 'boolean'],
        ]);

        if (!empty($validated['is_default'])) {
            Address::where('user_id', $address->user_id)->update(['is_default' => false]);
        }

        $address->update($validated);

        return response()->json([
            'success' => true,
            'message' => 'Cập nhật địa chỉ thành công',
            'data' => $address->fresh(),
        ]);
    }

    public function destroy(int $id): JsonResponse
    {
        $address = Address::find($id);
        if (!$address) {
            return response()->json(['success' => false, 'message' => 'Không tìm thấy địa chỉ'], 404);
        }

        $address->delete();

        return response()->json([
            'success' => true,
            'message' => 'Đã xóa địa chỉ thành công',
        ]);
    }

    public function setDefault(int $id): JsonResponse
    {
        $address = Address::find($id);
        if (!$address) {
            return response()->json(['success' => false, 'message' => 'Không tìm thấy địa chỉ'], 404);
        }

        Address::where('user_id', $address->user_id)->update(['is_default' => false]);
        $address->is_default = true;
        $address->save();

        return response()->json([
            'success' => true,
            'message' => 'Đã đặt làm địa chỉ mặc định',
            'data' => $address,
        ]);
    }
}
