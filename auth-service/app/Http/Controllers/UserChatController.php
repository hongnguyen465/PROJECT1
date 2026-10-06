<?php

namespace App\Http\Controllers;

use App\Models\Message;
use App\Models\User;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

class UserChatController extends Controller
{
    private function getAdminId(): int
    {
        $admin = User::where('role', 'admin')->first();
        return $admin ? $admin->id : 1;
    }

    public function getMessages(Request $request): JsonResponse
    {
        $user = auth('api')->user();
        $userId = $user ? $user->id : (int) $request->input('user_id');

        if (!$userId) {
            return response()->json(['success' => true, 'data' => []]);
        }

        $adminId = $this->getAdminId();

        $messages = Message::with(['sender', 'receiver'])
            ->where(function ($q) use ($userId, $adminId) {
                $q->where('sender_id', $userId)->where('receiver_id', $adminId);
            })
            ->orWhere(function ($q) use ($userId, $adminId) {
                $q->where('sender_id', $adminId)->where('receiver_id', $userId);
            })
            ->orderBy('created_at', 'asc')
            ->get();

        return response()->json([
            'success' => true,
            'data' => $messages,
        ]);
    }

    public function send(Request $request): JsonResponse
    {
        $user = auth('api')->user();
        $userId = $user ? $user->id : (int) $request->input('user_id');

        $content = $request->input('message') ?? $request->input('content');
        if (empty(trim((string) $content))) {
            return response()->json(['success' => false, 'message' => 'Nội dung tin nhắn không được để trống'], 400);
        }

        if (!$userId) {
            // If guest, find or create guest user or use temporary user
            $userId = 2; // fallback to customer 1
        }

        $adminId = $this->getAdminId();

        $msg = Message::create([
            'sender_id' => $userId,
            'receiver_id' => $adminId,
            'content' => trim((string) $content),
            'is_read' => false,
        ]);

        $msg->load(['sender', 'receiver']);

        return response()->json([
            'success' => true,
            'message' => 'Gửi tin nhắn thành công',
            'data' => $msg,
        ], 201);
    }
}
