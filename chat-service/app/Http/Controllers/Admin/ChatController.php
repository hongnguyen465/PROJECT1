<?php

namespace App\Http\Controllers\Admin;

use App\Http\Controllers\Controller;
use App\Models\ChatFeedback;
use App\Models\Message;
use App\Models\User;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Http;
use Throwable;

class ChatController extends Controller
{
    /**
     * Xác định Admin ID hiện tại
     */
    private function resolveAdminId(Request $request): int
    {
        $adminId = $request->header('X-User-Id') ?? $request->input('admin_id');
        if ($adminId) {
            return (int) $adminId;
        }

        $authHeader = (string) $request->header('Authorization', '');
        if (str_starts_with($authHeader, 'Bearer ')) {
            $parts = explode('.', substr($authHeader, 7));
            if (count($parts) === 3) {
                $payload = json_decode(base64_decode(strtr($parts[1], '-_', '+/')), true);
                if (isset($payload['sub'])) {
                    return (int) $payload['sub'];
                }
            }
        }

        if (Auth::check()) {
            return (int) Auth::id();
        }

        try {
            $admin = User::where('role', 'admin')->first();
            if ($admin) {
                return (int) $admin->id;
            }
        } catch (Throwable $e) {}

        return 1;
    }

    /**
     * Lấy danh sách khách hàng đã nhắn tin kèm tin nhắn mới nhất và số tin chưa đọc (Tối ưu truy vấn SQL)
     */
    public function getUsers(Request $request): JsonResponse
    {
        $adminId = $this->resolveAdminId($request);

        // 1. Tìm tất cả ID khách hàng có tương tác với Admin/AI
        $userIds = Message::where(function ($q) use ($adminId) {
                $q->where('receiver_id', $adminId)->where('sender_id', '!=', $adminId);
            })
            ->orWhere(function ($q) use ($adminId) {
                $q->where('sender_id', $adminId)->where('receiver_id', '!=', $adminId);
            })
            ->orderByDesc('created_at')
            ->get()
            ->map(fn ($msg) => (int) ($msg->sender_id == $adminId ? $msg->receiver_id : $msg->sender_id))
            ->filter(fn ($id) => $id !== (int) $adminId)
            ->unique()
            ->values()
            ->toArray();

        if (empty($userIds)) {
            return response()->json([
                'success' => true,
                'message' => 'Chưa có cuộc trò chuyện nào.',
                'data' => [],
            ]);
        }

        // 2. Lấy thông tin chi tiết khách hàng từ DB auth hoặc API fallback
        $usersMap = [];
        try {
            $users = User::whereIn('id', $userIds)
                ->where('role', '!=', 'admin')
                ->select('id', 'name', 'email', 'phone', 'role', 'created_at')
                ->get();
            foreach ($users as $u) {
                $usersMap[$u->id] = $u;
            }
        } catch (Throwable $e) {
            $authUrl = rtrim((string) config('services.microservices.auth', 'http://127.0.0.1:8001'), '/');
            try {
                $res = Http::timeout(2)->get("{$authUrl}/api/users");
                if ($res->successful() && is_array($res->json('data'))) {
                    foreach ($res->json('data') as $item) {
                        if (in_array((int)$item['id'], $userIds)) {
                            $usersMap[$item['id']] = (object)$item;
                        }
                    }
                }
            } catch (Throwable $ex) {}
        }

        // 3. Truy vấn gom nhóm số tin nhắn chưa đọc của từng user (Tránh N+1 query)
        $unreadCounts = Message::whereIn('sender_id', $userIds)
            ->where('receiver_id', $adminId)
            ->where('is_read', false)
            ->select('sender_id', DB::raw('count(*) as total'))
            ->groupBy('sender_id')
            ->pluck('total', 'sender_id')
            ->toArray();

        // 4. Định dạng dữ liệu hoàn chỉnh
        $usersWithDetails = collect($userIds)->map(function ($userId) use ($adminId, $usersMap, $unreadCounts) {
            $user = $usersMap[$userId] ?? null;

            $lastMsg = Message::where(function ($q) use ($userId, $adminId) {
                $q->where('sender_id', $userId)->where('receiver_id', $adminId);
            })->orWhere(function ($q) use ($userId, $adminId) {
                $q->where('sender_id', $adminId)->where('receiver_id', $userId);
            })->orderByDesc('created_at')->first();

            return [
                'id' => $userId,
                'name' => $user ? ($user->name ?? "Khách hàng #{$userId}") : "Khách hàng #{$userId}",
                'email' => $user ? ($user->email ?? '') : '',
                'phone' => $user ? ($user->phone ?? ($user->phone_number ?? '')) : '',
                'phone_number' => $user ? ($user->phone ?? ($user->phone_number ?? '')) : '',
                'avatar' => null,
                'role' => $user ? ($user->role ?? 'customer') : 'customer',
                'last_message' => $lastMsg ? $lastMsg->content : '',
                'last_message_time' => $lastMsg ? $lastMsg->created_at : null,
                'unread_count' => (int) ($unreadCounts[$userId] ?? 0),
            ];
        })->sortByDesc(fn ($item) => $item['last_message_time'] ? strtotime((string)$item['last_message_time']) : 0)->values();

        return response()->json([
            'success' => true,
            'message' => 'Lấy danh sách người dùng nhắn tin thành công.',
            'data' => $usersWithDetails,
        ]);
    }

    /**
     * Tìm kiếm khách hàng theo tên, email, số điện thoại để Admin chủ động nhắn tin
     */
    public function searchCustomers(Request $request): JsonResponse
    {
        $adminId = $this->resolveAdminId($request);
        $query = trim((string) $request->input('query', ''));

        $customers = collect();
        try {
            $customers = User::where('id', '!=', $adminId)
                ->where('role', '!=', 'admin')
                ->when($query !== '', function ($q) use ($query) {
                    $q->where(function ($sub) use ($query) {
                        $sub->where('name', 'like', "%{$query}%")
                            ->orWhere('email', 'like', "%{$query}%")
                            ->orWhere('phone', 'like', "%{$query}%");
                    });
                })
                ->select('id', 'name', 'email', 'phone', 'role', 'created_at')
                ->limit(30)
                ->get();
        } catch (Throwable $e) {
            $authUrl = rtrim((string) config('services.microservices.auth', 'http://127.0.0.1:8001'), '/');
            try {
                $response = Http::timeout(2)->get("{$authUrl}/api/users", ['search' => $query]);
                if ($response->successful()) {
                    $customers = collect($response->json('data') ?? []);
                }
            } catch (Throwable $ex) {}
        }

        $customersWithDetails = $customers->map(function ($user) use ($adminId) {
            $userId = is_array($user) ? $user['id'] : $user->id;
            $userName = is_array($user) ? $user['name'] : $user->name;
            $userEmail = is_array($user) ? ($user['email'] ?? '') : ($user->email ?? '');
            $userPhone = is_array($user) ? ($user['phone'] ?? ($user['phone_number'] ?? '')) : ($user->phone ?? '');
            $userRole = is_array($user) ? ($user['role'] ?? 'customer') : ($user->role ?? 'customer');

            $lastMsg = Message::where(function ($q) use ($userId, $adminId) {
                $q->where('sender_id', $userId)->where('receiver_id', $adminId);
            })->orWhere(function ($q) use ($userId, $adminId) {
                $q->where('sender_id', $adminId)->where('receiver_id', $userId);
            })->orderByDesc('created_at')->first();

            $unreadCount = Message::where('sender_id', $userId)
                ->where('receiver_id', $adminId)
                ->where('is_read', false)
                ->count();

            return [
                'id' => $userId,
                'name' => $userName,
                'email' => $userEmail,
                'phone' => $userPhone,
                'phone_number' => $userPhone,
                'avatar' => null,
                'role' => $userRole,
                'last_message' => $lastMsg ? $lastMsg->content : '',
                'last_message_time' => $lastMsg ? $lastMsg->created_at : null,
                'unread_count' => $unreadCount,
            ];
        });

        return response()->json([
            'success' => true,
            'message' => 'Tìm kiếm khách hàng thành công.',
            'data' => $customersWithDetails,
        ]);
    }

    /**
     * Lấy thông tin 1 User để Admin mở cuộc trò chuyện
     */
    public function getUserDetail(Request $request, $userId): JsonResponse
    {
        $user = null;
        try {
            $user = User::select('id', 'name', 'email', 'phone', 'role', 'created_at')->find($userId);
        } catch (Throwable $e) {}

        if (!$user) {
            $authUrl = rtrim((string) config('services.microservices.auth', 'http://127.0.0.1:8001'), '/');
            try {
                $response = Http::timeout(2)->get("{$authUrl}/api/users/{$userId}");
                if ($response->successful()) {
                    $userData = $response->json('data') ?? $response->json('user');
                    if ($userData) $user = (object)$userData;
                }
            } catch (Throwable $ex) {}
        }

        if (!$user) {
            return response()->json([
                'success' => false,
                'message' => 'Không tìm thấy khách hàng.',
            ], 404);
        }

        $adminId = $this->resolveAdminId($request);
        $lastMsg = Message::where(function ($q) use ($userId, $adminId) {
            $q->where('sender_id', $userId)->where('receiver_id', $adminId);
        })->orWhere(function ($q) use ($userId, $adminId) {
            $q->where('sender_id', $adminId)->where('receiver_id', $userId);
        })->orderByDesc('created_at')->first();

        return response()->json([
            'success' => true,
            'data' => [
                'id' => is_array($user) ? $user['id'] : $user->id,
                'name' => is_array($user) ? $user['name'] : $user->name,
                'email' => is_array($user) ? ($user['email'] ?? '') : ($user->email ?? ''),
                'phone' => is_array($user) ? ($user['phone'] ?? ($user['phone_number'] ?? '')) : ($user->phone ?? ''),
                'phone_number' => is_array($user) ? ($user['phone'] ?? ($user['phone_number'] ?? '')) : ($user->phone ?? ''),
                'avatar' => null,
                'role' => is_array($user) ? ($user['role'] ?? 'customer') : ($user->role ?? 'customer'),
                'last_message' => $lastMsg ? $lastMsg->content : '',
                'last_message_time' => $lastMsg ? $lastMsg->created_at : null,
                'unread_count' => 0,
            ],
        ]);
    }

    /**
     * Lấy lịch sử tin nhắn của một User cụ thể và đánh dấu đã đọc
     */
    public function getMessages(Request $request, $userId): JsonResponse
    {
        $adminId = $this->resolveAdminId($request);

        // Đánh dấu tin nhắn từ user gửi tới admin là đã đọc
        Message::where('sender_id', $userId)
            ->where('receiver_id', $adminId)
            ->where('is_read', false)
            ->update(['is_read' => true]);

        $messages = Message::where(function ($q) use ($userId, $adminId) {
                $q->where('sender_id', $userId)->where('receiver_id', $adminId);
            })
            ->orWhere(function ($q) use ($userId, $adminId) {
                $q->where('sender_id', $adminId)->where('receiver_id', $userId);
            })
            ->orderBy('created_at', 'asc')
            ->orderBy('id', 'asc')
            ->get();

        return response()->json([
            'success' => true,
            'message' => 'Lấy lịch sử tin nhắn thành công.',
            'data' => $messages,
        ]);
    }

    /**
     * Admin gửi tin nhắn phản hồi cho User
     */
    public function send(Request $request): JsonResponse
    {
        $request->validate([
            'user_id' => 'required',
            'message' => 'sometimes|nullable|string',
            'content' => 'sometimes|nullable|string',
        ]);

        $content = trim((string) ($request->input('message') ?? $request->input('content') ?? ''));
        $attachmentUrl = $request->input('attachment_url') ?? $request->input('file_url');
        $attachmentType = $request->input('attachment_type') ?? ($attachmentUrl ? 'image' : null);
        $attachmentName = $request->input('attachment_name');

        if ($request->hasFile('file')) {
            $file = $request->file('file');
            $fileName = time() . '_' . preg_replace('/[^a-zA-Z0-9._-]/', '', $file->getClientOriginalName());
            $destinationPath = public_path('uploads/chat');
            if (!file_exists($destinationPath)) {
                mkdir($destinationPath, 0777, true);
            }
            $file->move($destinationPath, $fileName);
            $attachmentUrl = '/uploads/chat/' . $fileName;
            $attachmentName = $file->getClientOriginalName();
            $mime = $file->getClientMimeType();
            $attachmentType = str_starts_with($mime, 'image/') ? 'image' : 'file';
        }

        if (empty($content) && empty($attachmentUrl)) {
            return response()->json([
                'success' => false,
                'message' => 'Nội dung tin nhắn không được để trống.',
            ], 400);
        }

        $adminId = $this->resolveAdminId($request);
        $targetUserId = (int)$request->input('user_id');

        $message = Message::create([
            'sender_id' => $adminId,
            'receiver_id' => $targetUserId,
            'content' => $content ?: '[Tệp đính kèm]',
            'sender_type' => 'ADMIN',
            'attachment_url' => $attachmentUrl,
            'attachment_type' => $attachmentType,
            'attachment_name' => $attachmentName,
            'is_read' => true,
        ]);

        return response()->json([
            'success' => true,
            'message' => 'Admin gửi tin nhắn thành công.',
            'data' => $message,
            'id' => $message->id,
            'sender_id' => $message->sender_id,
            'receiver_id' => $message->receiver_id,
            'content' => $message->content,
            'sender_type' => $message->sender_type,
            'attachment_url' => $message->attachment_url,
            'attachment_type' => $message->attachment_type,
            'attachment_name' => $message->attachment_name,
            'is_read' => $message->is_read,
            'created_at' => $message->created_at,
        ]);
    }

    /**
     * Lấy tổng số tin nhắn chưa đọc cho Admin (Badge chuông thông báo)
     */
    public function getUnreadCount(Request $request): JsonResponse
    {
        $adminId = $this->resolveAdminId($request);

        $totalUnread = Message::where('receiver_id', $adminId)
            ->where('is_read', false)
            ->count();

        $recentMessages = Message::where('receiver_id', $adminId)
            ->where('is_read', false)
            ->orderByDesc('created_at')
            ->limit(5)
            ->get();

        return response()->json([
            'success' => true,
            'unread_count' => $totalUnread,
            'count' => $totalUnread,
            'data' => [
                'unread_count' => $totalUnread,
                'recent_messages' => $recentMessages,
            ],
        ]);
    }

    /**
     * Đánh dấu toàn bộ tin nhắn của một User là đã đọc
     */
    public function markAsRead(Request $request, $userId): JsonResponse
    {
        $adminId = $this->resolveAdminId($request);

        Message::where('sender_id', $userId)
            ->where('receiver_id', $adminId)
            ->where('is_read', false)
            ->update(['is_read' => true]);

        return response()->json([
            'success' => true,
            'message' => 'Đã đánh dấu tin nhắn là đã đọc.',
        ]);
    }

    /**
     * Lấy danh sách đánh giá hài lòng (CSAT) và thống kê điểm trung bình
     */
    public function getFeedbacks(Request $request): JsonResponse
    {
        $feedbacks = ChatFeedback::orderByDesc('created_at')->limit(50)->get();
        $total = ChatFeedback::count();
        $avg = $total > 0 ? round((float)ChatFeedback::avg('rating'), 1) : 5.0;

        $ratingCounts = [
            5 => ChatFeedback::where('rating', 5)->count(),
            4 => ChatFeedback::where('rating', 4)->count(),
            3 => ChatFeedback::where('rating', 3)->count(),
            2 => ChatFeedback::where('rating', 2)->count(),
            1 => ChatFeedback::where('rating', 1)->count(),
        ];

        return response()->json([
            'success' => true,
            'data' => [
                'feedbacks' => $feedbacks,
                'stats' => [
                    'total' => $total,
                    'average_rating' => $avg,
                    'rating_counts' => $ratingCounts,
                ],
            ],
        ]);
    }
}
