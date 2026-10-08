<?php

namespace App\Http\Controllers\User;

use App\Http\Controllers\Controller;
use App\Models\ChatFeedback;
use App\Models\Message;
use App\Services\GeminiService;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Throwable;

class ChatController extends Controller
{
    public function __construct(
        protected GeminiService $geminiService
    ) {}

    /**
     * Xác định ID người dùng hiện tại từ Request / Header / JWT Token
     */
    private function resolveUserId(Request $request): ?int
    {
        $id = $request->input('sender_id') 
            ?? $request->input('user_id') 
            ?? $request->query('user_id') 
            ?? $request->header('X-User-Id');

        if ($id) {
            return (int) $id;
        }

        if (Auth::check()) {
            return (int) Auth::id();
        }

        // Thử giải mã JWT payload nếu có trong Authorization header
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

        return null;
    }

    /**
     * Xử lý lưu trữ tệp đính kèm (Multipart file hoặc Base64 Data URL)
     * @return array{url: ?string, type: ?string, name: ?string, local_path: ?string, mime: ?string}
     */
    private function processAttachment(Request $request): array
    {
        $attachmentUrl = $request->input('attachment_url') ?? $request->input('file_url');
        $attachmentType = $request->input('attachment_type');
        $attachmentName = $request->input('attachment_name');
        $localPath = null;
        $mimeType = null;

        $uploadDir = public_path('uploads/chat');
        if (!file_exists($uploadDir)) {
            mkdir($uploadDir, 0777, true);
        }

        // 1. Trường hợp gửi Multipart Form File
        if ($request->hasFile('file')) {
            $file = $request->file('file');
            $fileName = time() . '_' . preg_replace('/[^a-zA-Z0-9._-]/', '', $file->getClientOriginalName());
            $file->move($uploadDir, $fileName);

            $localPath = $uploadDir . DIRECTORY_SEPARATOR . $fileName;
            $attachmentUrl = '/uploads/chat/' . $fileName;
            $attachmentName = $file->getClientOriginalName();
            $mimeType = $file->getClientMimeType();
            $attachmentType = str_starts_with($mimeType, 'image/') ? 'image' : 'file';
        }
        // 2. Trường hợp gửi chuỗi Base64 Data URL (data:image/...)
        elseif (!empty($attachmentUrl) && str_starts_with($attachmentUrl, 'data:image/')) {
            if (preg_match('/^data:(image\/[a-zA-Z0-9\+\-\.]+);base64,(.*)$/s', $attachmentUrl, $matches)) {
                $mimeType = $matches[1];
                $binary = base64_decode($matches[2]);
                if ($binary !== false) {
                    $ext = match ($mimeType) {
                        'image/png' => 'png',
                        'image/webp' => 'webp',
                        'image/gif' => 'gif',
                        default => 'jpg',
                    };
                    $fileName = time() . '_' . uniqid() . '.' . $ext;
                    $savePath = $uploadDir . DIRECTORY_SEPARATOR . $fileName;
                    file_put_contents($savePath, $binary);

                    $localPath = $savePath;
                    $attachmentUrl = '/uploads/chat/' . $fileName;
                    $attachmentType = 'image';
                    $attachmentName = $attachmentName ?: ('image_' . date('Ymd_His') . '.' . $ext);
                }
            }
        }
        // 3. Trường hợp URL file tương đối đã có trên máy chủ
        elseif (!empty($attachmentUrl) && $attachmentType === 'image') {
            $cleanUrl = ltrim((string) parse_url($attachmentUrl, PHP_URL_PATH), '/');
            $candidatePath = public_path($cleanUrl);
            if (file_exists($candidatePath)) {
                $localPath = $candidatePath;
                $mimeType = mime_content_type($candidatePath) ?: 'image/jpeg';
            }
        }

        return [
            'url' => $attachmentUrl,
            'type' => $attachmentType ?? ($attachmentUrl ? 'image' : null),
            'name' => $attachmentName,
            'local_path' => $localPath,
            'mime' => $mimeType,
        ];
    }

    /**
     * Gửi tin nhắn từ Khách hàng và kích hoạt Gemini AI tự động phản hồi
     */
    public function send(Request $request): JsonResponse
    {
        $messageText = trim((string) ($request->input('message') ?? $request->input('content') ?? ''));
        $attachment = $this->processAttachment($request);

        // Kiểm tra hợp lệ nội dung
        if (empty($messageText) && empty($attachment['url'])) {
            return response()->json([
                'success' => false,
                'message' => 'Nội dung tin nhắn hoặc tệp đính kèm không được để trống.',
            ], 400);
        }

        $senderId = $this->resolveUserId($request);
        if (!$senderId) {
            return response()->json([
                'success' => false,
                'message' => 'Vui lòng đăng nhập để gửi tin nhắn.',
            ], 401);
        }

        $adminId = 1;

        try {
            $promptText = $messageText;
            if (empty($promptText) && !empty($attachment['url'])) {
                $promptText = $attachment['type'] === 'image' ? '[Hình ảnh]' : '[Tệp đính kèm]';
            }

            // 1. Lưu tin nhắn của khách hàng vào database
            $userMessage = Message::create([
                'sender_id' => $senderId,
                'receiver_id' => $adminId,
                'content' => $promptText,
                'sender_type' => 'CUSTOMER',
                'attachment_url' => $attachment['url'],
                'attachment_type' => $attachment['type'],
                'attachment_name' => $attachment['name'],
                'is_read' => false,
            ]);

            // 2. Kích hoạt Gemini AI (Vision + Product Cards + Order Tracking)
            $aiResult = $this->geminiService->generateReply(
                $senderId,
                $promptText,
                $attachment['local_path'],
                $attachment['mime']
            );

            $aiReplyText = $aiResult['text'] ?? 'Chào bạn! Mình có thể giúp gì cho bạn hôm nay?';
            $suggestedProducts = $aiResult['suggested_products'] ?? [];
            $orderTracking = $aiResult['order_tracking'] ?? null;

            $metadata = null;
            if (!empty($suggestedProducts) || !empty($orderTracking)) {
                $metadata = array_filter([
                    'suggested_products' => !empty($suggestedProducts) ? $suggestedProducts : null,
                    'order_tracking' => $orderTracking,
                ]);
            }

            // 3. Lưu câu trả lời của AI vào database
            $aiMessage = Message::create([
                'sender_id' => $adminId,
                'receiver_id' => $senderId,
                'content' => $aiReplyText,
                'sender_type' => 'AI',
                'metadata' => $metadata,
                'is_read' => false,
            ]);

            return response()->json([
                'success' => true,
                'message' => 'Gửi tin nhắn thành công.',
                'data' => $userMessage,
                'id' => $userMessage->id,
                'sender_id' => $userMessage->sender_id,
                'receiver_id' => $userMessage->receiver_id,
                'content' => $userMessage->content,
                'sender_type' => $userMessage->sender_type,
                'attachment_url' => $userMessage->attachment_url,
                'attachment_type' => $userMessage->attachment_type,
                'attachment_name' => $userMessage->attachment_name,
                'metadata' => $userMessage->metadata,
                'is_read' => $userMessage->is_read,
                'created_at' => $userMessage->created_at,
                'ai_response' => [
                    'id' => $aiMessage->id,
                    'content' => $aiMessage->content,
                    'sender_type' => 'AI',
                    'metadata' => $aiMessage->metadata,
                    'created_at' => $aiMessage->created_at,
                ],
            ]);
        } catch (Throwable $e) {
            return response()->json([
                'success' => false,
                'message' => 'Không thể gửi tin nhắn: ' . $e->getMessage(),
            ], 500);
        }
    }

    /**
     * Lấy toàn bộ lịch sử tin nhắn của User với Admin/AI
     */
    public function getMessages(Request $request): JsonResponse
    {
        $userId = $this->resolveUserId($request);
        if (!$userId) {
            return response()->json([
                'success' => false,
                'message' => 'Vui lòng đăng nhập để xem tin nhắn.',
                'data' => [],
            ], 401);
        }

        $adminId = 1;

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
     * Tiếp nhận đánh giá hài lòng cuộc hội thoại (CSAT ⭐)
     */
    public function submitFeedback(Request $request): JsonResponse
    {
        $userId = $this->resolveUserId($request);
        if (!$userId) {
            return response()->json([
                'success' => false,
                'message' => 'Vui lòng đăng nhập để đánh giá.',
            ], 401);
        }

        $validated = $request->validate([
            'rating' => 'required|integer|min:1|max:5',
            'message_id' => 'sometimes|nullable|integer',
            'feedback_type' => 'sometimes|nullable|string',
            'comment' => 'sometimes|nullable|string|max:500',
            'tags' => 'sometimes|nullable|array',
        ]);

        try {
            $feedback = ChatFeedback::create([
                'user_id' => $userId,
                'message_id' => $validated['message_id'] ?? null,
                'rating' => (int) $validated['rating'],
                'feedback_type' => $validated['feedback_type'] ?? 'ai',
                'comment' => $validated['comment'] ?? null,
                'tags' => $validated['tags'] ?? [],
            ]);

            return response()->json([
                'success' => true,
                'message' => 'Cảm ơn bạn đã gửi đánh giá hài lòng!',
                'data' => $feedback,
            ]);
        } catch (Throwable $e) {
            return response()->json([
                'success' => false,
                'message' => 'Không thể lưu đánh giá: ' . $e->getMessage(),
            ], 500);
        }
    }
}
