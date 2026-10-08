<?php

namespace App\Services;

use App\Models\Message;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;
use Throwable;

class GeminiService
{
    protected string $apiKey;
    protected string $model;
    protected string $catalogServiceUrl;
    protected string $orderServiceUrl;

    public function __construct()
    {
        $this->apiKey = (string) config('services.gemini.api_key', env('GEMINI_API_KEY', ''));
        $this->model = (string) config('services.gemini.model', env('GEMINI_MODEL', 'gemini-3.5-flash-lite'));
        $this->catalogServiceUrl = rtrim((string) config('services.microservices.catalog', 'http://127.0.0.1:8002'), '/');
        $this->orderServiceUrl = rtrim((string) config('services.microservices.order', 'http://127.0.0.1:8003'), '/');
    }

    /**
     * Kiểm tra xem API Key của Gemini có hợp lệ hay chỉ là chuỗi placeholder
     */
    public function hasValidApiKey(): bool
    {
        $key = trim($this->apiKey);
        if (empty($key)) {
            return false;
        }
        if (
            $key === 'your_gemini_api_key_here' || 
            $key === 'your-api-key' || 
            $key === 'GEMINI_API_KEY' || 
            str_starts_with($key, 'your_') || 
            str_starts_with($key, 'YOUR_') ||
            strlen($key) < 15
        ) {
            return false;
        }
        return true;
    }

    /**
     * Tạo câu trả lời tự động bằng Gemini AI (Hỗ trợ Multimodal Vision + Gợi ý sản phẩm + Tra cứu đơn hàng)
     * 
     * @param int $userId
     * @param string $incomingMessage
     * @param string|null $imagePath Đường dẫn file ảnh trên server nếu có
     * @param string|null $imageMime MIME type của ảnh (image/jpeg, image/png, ...)
     * @return array{text: string, suggested_products: array, order_tracking: ?array}
     */
    public function generateReply(int $userId, string $incomingMessage, ?string $imagePath = null, ?string $imageMime = null): array
    {
        // 1. Kiểm tra hình ảnh đính kèm để kích hoạt Gemini Vision
        $hasImage = !empty($imagePath) && file_exists($imagePath);

        // 2. Tra cứu đơn hàng trực quan nếu khách hàng hỏi về đơn
        $orderTracking = $this->findOrderTracking($userId, $incomingMessage);

        // 3. Tìm sản phẩm phù hợp từ kho hàng
        $suggestedProducts = $this->findSuggestedProducts($incomingMessage);

        // 4. Lấy ngữ cảnh 6 tin nhắn gần nhất để giữ mạch hội thoại
        $history = collect();
        try {
            $history = Message::where(function ($q) use ($userId) {
                    $q->where('sender_id', $userId)->orWhere('receiver_id', $userId);
                })
                ->orderByDesc('created_at')
                ->orderByDesc('id')
                ->limit(6)
                ->get()
                ->reverse();
        } catch (Throwable $e) {
            Log::warning("Could not fetch chat history: " . $e->getMessage());
        }

        // 5. Thu thập dữ liệu thực tế từ các microservice (Catalog, Coupons, Orders, Weather)
        $dynamicContext = $this->gatherDynamicContext($userId, $incomingMessage);

        // 6. Nếu chưa có API Key hợp lệ -> Sử dụng phản hồi dự phòng thông minh (Fallback)
        if (!$this->hasValidApiKey()) {
            return [
                'text' => $this->fallbackReply($userId, $incomingMessage, $dynamicContext, $hasImage),
                'suggested_products' => $suggestedProducts,
                'order_tracking' => $orderTracking,
            ];
        }

        // 7. Chuẩn bị System Instruction và danh sách Candidate Models
        $candidateModels = array_values(array_filter(
            array_unique([$this->model, 'gemini-3.5-flash-lite', 'gemini-3.7-flash', 'gemini-3.8-flash']),
            fn ($m) => !empty($m) && !str_contains($m, '2.5') && !str_contains($m, '1.5')
        ));

        if (empty($candidateModels)) {
            $candidateModels = ['gemini-3.5-flash-lite', 'gemini-3.7-flash'];
        }

        $systemInstruction = "Bạn là trợ lý ảo AI thông minh, nhiệt tình và chuyên nghiệp của website STRIKER (cửa hàng chuyên giày bóng đá chính hãng, áo đấu và phụ kiện thể thao tại Việt Nam).\n\n"
            . "QUY TẮC & NĂNG LỰC TRẢ LỜI CỦA BẠN:\n"
            . "1. NĂNG LỰC GEMINI VISION (PHÂN TÍCH ẢNH GIÀY THÔNG MINH):\n"
            . "   - Nếu khách hàng gửi ảnh một đôi giày hoặc sản phẩm thể thao, bạn hãy quan sát kỹ ảnh: nhận diện chính xác thương hiệu (Nike, Adidas, Puma, Mizuno...), dòng giày (Mercurial, Predator, Phantom, Tiempo, Speedportal, Future...), phiên bản, màu sắc và loại đinh (TF sân nhân tạo, FG sân tự nhiên, IC futsal).\n"
            . "   - Nhận xét ưu điểm nổi bật của mẫu giày này (cảm giác bóng, tốc độ, độ ôm chân, form chân thon hay bè).\n"
            . "   - Giới thiệu rằng STRIKER có sẵn các mẫu giày tương tự trong kho với giá tốt và chính sách đổi size 30 ngày.\n\n"
            . "2. TRA CỨU ĐƠN HÀNG TRỰC QUAN:\n"
            . "   - Khi khách hỏi về đơn hàng hoặc mã vận đơn, hãy thông báo ngắn gọn tình trạng đơn hàng và chúc khách sớm nhận được hàng.\n\n"
            . "3. TƯ VẤN SẢN PHẨM & CỬA HÀNG:\n"
            . "   - Tư vấn chính xác về giá bán, hướng dẫn chọn size chuẩn (chân bè tăng 0.5-1 size), chính sách bảo hành 6 tháng, đổi trả 30 ngày, giao hàng GHN 2-4 ngày.\n"
            . "   - Báo đúng các mã voucher khuyến mãi đang có theo dữ liệu được cung cấp.\n\n"
            . "4. TRẢ LỜI MỌI LĨNH VỰC KHÁC:\n"
            . "   - Trả lời xuất sắc tất cả câu hỏi ngoài lề (Toán học 1+1=2, khoa học, thể thao, văn hóa, thời tiết, địa lý, đời sống...).\n\n"
            . "5. PHONG CÁCH:\n"
            . "   - Thân thiện, lịch sự, chuẩn tiếng Việt, có emoji sinh động (⚽, 👟, 🏆, ✨, 📦), súc tích, dễ nhìn trên khung chat.\n\n"
            . "DỮ LIỆU THỰC TẾ HỆ THỐNG VÀ THỜI GIAN THỰC HIỆN TẠI:\n" . $dynamicContext;

        // Xây dựng mảng nội dung gửi đến Gemini API
        $contents = [];
        foreach ($history as $msg) {
            $role = (strtoupper((string)$msg->sender_type) === 'CUSTOMER' || $msg->sender_id === $userId) ? 'user' : 'model';
            $contents[] = [
                'role' => $role,
                'parts' => [['text' => (string) $msg->content]],
            ];
        }

        // Xây dựng parts cho tin nhắn hiện tại (kèm ảnh base64 nếu có)
        $currentParts = [];
        if ($hasImage) {
            try {
                $imageData = base64_encode(file_get_contents($imagePath));
                $mime = $imageMime ?: (mime_content_type($imagePath) ?: 'image/jpeg');
                $currentParts[] = [
                    'inline_data' => [
                        'mime_type' => $mime,
                        'data' => $imageData,
                    ],
                ];
            } catch (Throwable $e) {
                Log::warning("Gemini Vision image read failed: " . $e->getMessage());
            }
        }

        $userPrompt = $incomingMessage;
        if ($hasImage) {
            if (empty(trim($incomingMessage)) || str_starts_with($incomingMessage, '[Đã gửi') || $incomingMessage === '[Hình ảnh]' || $incomingMessage === '[Tệp đính kèm]') {
                $userPrompt = "Đây là bức ảnh sản phẩm/giày do khách hàng gửi đến. Hãy quan sát và phân tích thật kỹ hình ảnh: nhận diện chuẩn xác thương hiệu, kiểu dáng, phối màu, loại đế (giày bóng đá TF/FG/IC hay giày thể thao sneakers), đánh giá form chân và tư vấn mẫu giày này cho khách hàng một cách chuyên nghiệp và nhiệt tình.";
            } else {
                $userPrompt = "Hình ảnh đính kèm: [Ảnh sản phẩm do khách hàng gửi]. Nội dung khách hỏi: \"" . $incomingMessage . "\". Hãy quan sát hình ảnh và giải đáp câu hỏi của khách hàng một cách chi tiết.";
            }
        }

        $currentParts[] = ['text' => $userPrompt];
        $contents[] = ['role' => 'user', 'parts' => $currentParts];

        // 8. Thực hiện gọi Gemini API
        $timeoutSec = $hasImage ? 6 : 3;
        foreach ($candidateModels as $currentModel) {
            try {
                $url = "https://generativelanguage.googleapis.com/v1beta/models/{$currentModel}:generateContent?key={$this->apiKey}";
                $response = Http::withoutVerifying()
                    ->timeout($timeoutSec)
                    ->withHeaders(['Content-Type' => 'application/json'])
                    ->post($url, [
                        'system_instruction' => ['parts' => [['text' => $systemInstruction]]],
                        'contents' => $contents,
                        'generationConfig' => [
                            'temperature' => 0.7,
                            'maxOutputTokens' => 1000,
                        ],
                    ]);

                if ($response->successful()) {
                    $replyText = $response->json('candidates.0.content.parts.0.text');
                    if (!empty($replyText)) {
                        if ($hasImage && empty($suggestedProducts)) {
                            $suggestedProducts = $this->findSuggestedProducts($replyText);
                        }

                        return [
                            'text' => trim($replyText),
                            'suggested_products' => $suggestedProducts,
                            'order_tracking' => $orderTracking,
                        ];
                    }
                }

                // Nếu API key sai, không thử lại các model khác để tiết kiệm thời gian
                $body = $response->body();
                if ($response->status() === 400 && (str_contains($body, 'API_KEY_INVALID') || str_contains($body, 'API key not valid'))) {
                    Log::warning("Gemini API key is invalid, using smart fallback.");
                    break;
                }
            } catch (Throwable $e) {
                Log::warning("Gemini model {$currentModel} failed: " . $e->getMessage());
            }
        }

        return [
            'text' => $this->fallbackReply($userId, $incomingMessage, $dynamicContext, $hasImage),
            'suggested_products' => $suggestedProducts,
            'order_tracking' => $orderTracking,
        ];
    }

    /**
     * Tra cứu thông tin chi tiết đơn hàng trực quan khi khách hàng hỏi
     */
    public function findOrderTracking(int $userId, string $message): ?array
    {
        $normalized = mb_strtolower(trim($message), 'UTF-8');

        $isOrderQuery = str_contains($normalized, 'đơn hàng') 
            || str_contains($normalized, 'đơn của tôi') 
            || str_contains($normalized, 'kiểm tra đơn')
            || str_contains($normalized, 'tra cứu đơn')
            || str_contains($normalized, 'mã đơn')
            || str_contains($normalized, 'vận chuyển')
            || str_contains($normalized, 'giao hàng')
            || preg_match('/#\s*(\d+)/', $normalized)
            || preg_match('/str_ord_\d+/i', $normalized);

        if (!$isOrderQuery) {
            return null;
        }

        try {
            $res = Http::withoutVerifying()->timeout(2)->get("{$this->orderServiceUrl}/api/orders", ['user_id' => $userId]);
            if (!$res->successful() || empty($res->json('data'))) {
                return null;
            }

            $orders = $res->json('data');
            if (!is_array($orders) || empty($orders)) {
                return null;
            }

            $targetOrder = null;

            // Tìm theo ID hoặc mã đơn cụ thể nếu có
            if (preg_match('/#\s*(\d+)/', $normalized, $matches) || preg_match('/đơn\s*(\d+)/i', $normalized, $matches)) {
                $searchId = (int)$matches[1];
                foreach ($orders as $ord) {
                    if ((int)$ord['id'] === $searchId || str_contains(strval($ord['order_number'] ?? ''), (string)$searchId)) {
                        $targetOrder = $ord;
                        break;
                    }
                }
            }

            if (!$targetOrder) {
                $targetOrder = $orders[0];
            }

            $status = strtolower((string)($targetOrder['status'] ?? ($targetOrder['order_status'] ?? 'processing')));
            
            // Xây dựng timeline các mốc vận chuyển trực quan
            $steps = [
                [
                    'key' => 'placed',
                    'title' => 'Đặt hàng thành công',
                    'description' => 'Đơn hàng đã được hệ thống ghi nhận',
                    'completed' => true,
                    'time' => date('H:i d/m/Y', strtotime($targetOrder['created_at'] ?? 'now')),
                ],
                [
                    'key' => 'confirmed',
                    'title' => 'Đã xác nhận đơn',
                    'description' => 'Kho đang đóng gói sản phẩm',
                    'completed' => in_array($status, ['confirmed', 'processing', 'shipping', 'completed', 'delivered']),
                    'active' => in_array($status, ['confirmed', 'processing']),
                    'time' => in_array($status, ['confirmed', 'processing', 'shipping', 'completed', 'delivered']) ? 'Đã xác nhận' : null,
                ],
                [
                    'key' => 'shipping',
                    'title' => 'Đang vận chuyển (GHN)',
                    'description' => 'Bưu tá đang trên đường giao hàng',
                    'completed' => in_array($status, ['shipping', 'completed', 'delivered']),
                    'active' => $status === 'shipping',
                    'time' => in_array($status, ['shipping', 'completed', 'delivered']) ? 'Đang giao' : null,
                ],
                [
                    'key' => 'completed',
                    'title' => 'Giao hàng thành công',
                    'description' => 'Khách hàng đã nhận kiện hàng',
                    'completed' => in_array($status, ['completed', 'delivered']),
                    'active' => in_array($status, ['completed', 'delivered']),
                    'time' => in_array($status, ['completed', 'delivered']) ? 'Hoàn tất' : null,
                ],
            ];

            if ($status === 'cancelled') {
                $steps = [
                    [
                        'key' => 'placed',
                        'title' => 'Đặt hàng',
                        'description' => 'Đơn hàng đã được tạo',
                        'completed' => true,
                        'time' => date('H:i d/m/Y', strtotime($targetOrder['created_at'] ?? 'now')),
                    ],
                    [
                        'key' => 'cancelled',
                        'title' => 'Đã hủy đơn hàng',
                        'description' => 'Đơn hàng đã hủy theo yêu cầu',
                        'completed' => true,
                        'is_error' => true,
                        'time' => 'Đã hủy',
                    ],
                ];
            }

            $items = [];
            if (!empty($targetOrder['items']) && is_array($targetOrder['items'])) {
                foreach ($targetOrder['items'] as $it) {
                    $items[] = [
                        'id' => $it['id'] ?? 0,
                        'product_id' => $it['product_id'] ?? 0,
                        'name' => $it['product_name'] ?? ($it['name'] ?? 'Giày đá bóng chính hãng STRIKER'),
                        'image' => $it['product_image'] ?? ($it['image'] ?? ''),
                        'price' => (float)($it['price'] ?? 0),
                        'quantity' => (int)($it['quantity'] ?? 1),
                        'size' => $it['size'] ?? ($it['variant'] ?? null),
                    ];
                }
            }

            $statusLabels = [
                'pending' => 'Chờ xử lý',
                'processing' => 'Đang xử lý & đóng gói',
                'confirmed' => 'Đã xác nhận',
                'shipping' => 'Đang giao hàng',
                'completed' => 'Giao thành công',
                'delivered' => 'Giao thành công',
                'cancelled' => 'Đã hủy',
            ];

            return [
                'order_id' => (int)$targetOrder['id'],
                'order_number' => $targetOrder['order_number'] ?? ('#STR_' . $targetOrder['id']),
                'status' => $status,
                'status_label' => $statusLabels[$status] ?? 'Đang xử lý',
                'total_amount' => (float)($targetOrder['total_amount'] ?? 0),
                'shipping_fee' => (float)($targetOrder['shipping_fee'] ?? 0),
                'created_at' => $targetOrder['created_at'] ?? now()->toIso8601String(),
                'tracking_code' => $targetOrder['tracking_code'] ?? ('GHNVN' . str_pad((string)$targetOrder['id'], 6, '0', STR_PAD_LEFT)),
                'shipping_carrier' => 'Giao Hàng Nhanh (GHN Express)',
                'payment_method' => strtoupper($targetOrder['payment_method'] ?? 'COD'),
                'is_paid' => (bool)($targetOrder['is_paid'] ?? in_array($status, ['completed', 'delivered'])),
                'steps' => $steps,
                'items' => $items,
            ];
        } catch (Throwable $e) {
            Log::warning("Error finding order tracking: " . $e->getMessage());
        }

        return null;
    }

    /**
     * Tự động phát hiện và gợi ý các sản phẩm thực tế phù hợp từ Catalog
     */
    public function findSuggestedProducts(string $message): array
    {
        $normalized = mb_strtolower(trim($message), 'UTF-8');

        // Bỏ qua nếu là phép tính toán thuần túy
        if (preg_match('/^(\d+)\s*[\+\-\*\/xX]\s*(\d+)$/', $normalized)) {
            return [];
        }

        $products = Cache::remember('chat_catalog_all_products', 300, function () {
            try {
                $res = Http::withoutVerifying()->timeout(1.5)->get("{$this->catalogServiceUrl}/api/products", ['limit' => 30]);
                if ($res->successful() && is_array($res->json('data'))) {
                    return $res->json('data');
                }
            } catch (Throwable $e) {}
            return [];
        });

        if (empty($products)) return [];

        $matched = [];
        $isShoeQuery = str_contains($normalized, 'giày') 
            || str_contains($normalized, 'mẫu') 
            || str_contains($normalized, 'sản phẩm') 
            || str_contains($normalized, 'tư vấn') 
            || str_contains($normalized, 'mua') 
            || str_contains($normalized, 'size') 
            || str_contains($normalized, 'hot') 
            || str_contains($normalized, 'đá banh')
            || str_contains($normalized, 'ảnh')
            || str_contains($normalized, 'nike')
            || str_contains($normalized, 'adidas')
            || str_contains($normalized, 'puma')
            || str_contains($normalized, 'mizuno');

        foreach ($products as $p) {
            $pName = mb_strtolower($p['name'] ?? '', 'UTF-8');
            $pBrand = mb_strtolower($p['brand'] ?? '', 'UTF-8');
            $pTag = mb_strtolower($p['tag'] ?? '', 'UTF-8');
            $pDesc = mb_strtolower($p['description'] ?? '', 'UTF-8');

            $score = 0;

            // Khớp thương hiệu
            if (!empty($pBrand) && str_contains($normalized, $pBrand)) {
                $score += 6;
            }

            // Khớp dòng giày
            $lineKeywords = ['mercurial', 'predator', 'phantom', 'tiempo', 'crazyfast', 'speedportal', 'future', 'morelia', 'copa', 'ultra', 'king', 'áo', 'bóng', 'phụ kiện'];
            foreach ($lineKeywords as $kw) {
                if (str_contains($normalized, $kw) && (str_contains($pName, $kw) || str_contains($pDesc, $kw))) {
                    $score += 8;
                }
            }

            // Khớp loại đinh / mặt sân
            if ((str_contains($normalized, 'cỏ nhân tạo') || str_contains($normalized, 'tf')) && (str_contains($pName, 'tf') || str_contains($pDesc, 'tf') || str_contains($pDesc, 'nhân tạo'))) {
                $score += 7;
            }
            if ((str_contains($normalized, 'cỏ tự nhiên') || str_contains($normalized, 'fg')) && (str_contains($pName, 'fg') || str_contains($pDesc, 'fg') || str_contains($pDesc, 'tự nhiên'))) {
                $score += 7;
            }
            if (str_contains($normalized, 'futsal') || str_contains($normalized, 'ic')) {
                if (str_contains($pName, 'ic') || str_contains($pDesc, 'ic') || str_contains($pDesc, 'futsal')) {
                    $score += 7;
                }
            }

            // Ưu tiên sản phẩm bán chạy / hot
            if ($isShoeQuery && $score === 0) {
                if ($pTag === 'best seller' || $pTag === 'hot') {
                    $score += 2;
                }
            }

            if ($score > 0) {
                $img = $p['image_url'] ?? ($p['image'] ?? '');
                if (empty($img) && !empty($p['images']) && is_array($p['images'])) {
                    $img = $p['images'][0] ?? '';
                }

                $matched[] = [
                    'score' => $score,
                    'product' => [
                        'id' => (int) $p['id'],
                        'name' => $p['name'],
                        'brand' => $p['brand'] ?? 'STRIKER',
                        'tag' => $p['tag'] ?? null,
                        'price' => (float) ($p['price'] ?? 0),
                        'old_price' => !empty($p['old_price']) ? (float) $p['old_price'] : null,
                        'image' => $img,
                        'slug' => $p['slug'] ?? ('product-' . $p['id']),
                    ],
                ];
            }
        }

        if (empty($matched)) return [];

        usort($matched, fn ($a, $b) => $b['score'] <=> $a['score']);
        $top = array_slice($matched, 0, 3);
        return array_column($top, 'product');
    }

    /**
     * Thu thập dữ liệu thực tế từ các Microservice và API thời gian thực
     */
    protected function gatherDynamicContext(int $userId, string $message): string
    {
        $normalized = mb_strtolower(trim($message), 'UTF-8');

        // Cache thông tin tĩnh của cửa hàng trong 5 phút
        $baseContext = Cache::remember('chat_store_catalog_cache', 300, function () {
            $ctx = "[THÔNG TIN CƠ BẢN CỬA HÀNG STRIKER]\n"
                . "- Tên: STRIKER Football & Sportswear Store\n"
                . "- Hotline hỗ trợ: 0909.999.999 | Email: contact@striker.vn\n"
                . "- Địa chỉ showroom: 123 Cầu Giấy, Hà Nội & 456 Lê Văn Sỹ, Q.3, TP.HCM\n"
                . "- Chính sách vận chuyển: Giao hàng toàn quốc 2-4 ngày qua GHN, cho kiểm tra hàng trước khi nhận\n"
                . "- Chính sách bảo hành & đổi trả: Đổi size miễn phí 30 ngày (sản phẩm nguyên tem), bảo hành keo/chỉ 6 tháng\n"
                . "- Thanh toán: Tiền mặt khi nhận (COD), Ví điện tử MoMo, Thẻ ATM/Visa\n";

            // 1. Lấy dữ liệu sản phẩm / danh mục / thương hiệu từ catalog-service
            try {
                $catRes = Http::withoutVerifying()->timeout(1.5)->get("{$this->catalogServiceUrl}/api/categories");
                if ($catRes->successful() && !empty($catRes->json('data'))) {
                    $cats = array_column($catRes->json('data'), 'name');
                    $ctx .= "- Các danh mục: " . implode(', ', $cats) . "\n";
                }

                $brandRes = Http::withoutVerifying()->timeout(1.5)->get("{$this->catalogServiceUrl}/api/brands");
                if ($brandRes->successful() && !empty($brandRes->json('data'))) {
                    $brands = array_column($brandRes->json('data'), 'name');
                    $ctx .= "- Các thương hiệu: " . implode(', ', $brands) . "\n";
                }

                $prodRes = Http::withoutVerifying()->timeout(1.5)->get("{$this->catalogServiceUrl}/api/products", ['limit' => 10]);
                if ($prodRes->successful() && !empty($prodRes->json('data'))) {
                    $ctx .= "- Danh sách sản phẩm tiêu biểu:\n";
                    foreach ($prodRes->json('data') as $p) {
                        $priceStr = isset($p['price']) ? number_format($p['price']) . 'đ' : '';
                        $brandStr = !empty($p['brand']) ? " [Hãng: {$p['brand']}]" : '';
                        $ctx .= "  + ID #{$p['id']}: {$p['name']}{$brandStr} - Giá: {$priceStr}\n";
                    }
                }
            } catch (Throwable $e) {}

            // 2. Lấy danh sách Voucher thực tế từ order-service
            try {
                $couponRes = Http::withoutVerifying()->timeout(1.5)->get("{$this->orderServiceUrl}/api/coupons");
                if ($couponRes->successful() && !empty($couponRes->json('data'))) {
                    $ctx .= "- Mã giảm giá / Voucher đang áp dụng:\n";
                    foreach ($couponRes->json('data') as $c) {
                        $ctx .= "  + Mã '{$c['code']}': {$c['title']} ({$c['description']})\n";
                    }
                }
            } catch (Throwable $e) {}

            return $ctx;
        });

        $context = $baseContext;

        // 3. Nếu khách hỏi về đơn hàng -> Lấy dữ liệu đơn hàng thực tế
        if (str_contains($normalized, 'đơn hàng') || str_contains($normalized, 'đơn của tôi') || str_contains($normalized, 'vận chuyển') || str_contains($normalized, 'giao hàng') || str_contains($normalized, 'mã đơn')) {
            try {
                $orderRes = Http::withoutVerifying()->timeout(1.5)->get("{$this->orderServiceUrl}/api/orders", ['user_id' => $userId]);
                if ($orderRes->successful() && !empty($orderRes->json('data'))) {
                    $context .= "\n- Lịch sử đơn hàng của khách hàng (User ID #{$userId}):\n";
                    $orders = is_array($orderRes->json('data')) ? array_slice($orderRes->json('data'), 0, 3) : [];
                    foreach ($orders as $ord) {
                        $code = $ord['order_number'] ?? $ord['code'] ?? ('#' . $ord['id']);
                        $status = $ord['status'] ?? 'processing';
                        $total = isset($ord['total_amount']) ? number_format($ord['total_amount']) . 'đ' : '';
                        $track = !empty($ord['tracking_code']) ? " | GHN: {$ord['tracking_code']}" : '';
                        $context .= "  + Đơn {$code}: Trạng thái '{$status}', Tổng tiền {$total}{$track}\n";
                    }
                }
            } catch (Throwable $e) {}
        }

        // 4. Nếu hỏi về thời tiết thời gian thực
        if (str_contains($normalized, 'thời tiết') || str_contains($normalized, 'nhiệt độ') || str_contains($normalized, 'mưa không') || str_contains($normalized, 'trời hôm nay')) {
            $weatherData = $this->fetchRealtimeWeather($normalized);
            if (!empty($weatherData)) {
                $context .= "\n[DỮ LIỆU THỜI TIẾT THỜI GIAN THỰC TẠI VIỆT NAM HÔM NAY]:\n" . $weatherData . "\n";
            }
        }

        return $context;
    }

    /**
     * Lấy dữ liệu thời tiết thời gian thực chính xác từ Open-Meteo API
     */
    protected function fetchRealtimeWeather(string $query): string
    {
        $city = 'Hà Nội';
        $lat = 21.0285;
        $lon = 105.8542;

        if (str_contains($query, 'hồ chí minh') || str_contains($query, 'tphcm') || str_contains($query, 'hcm') || str_contains($query, 'sài gòn')) {
            $city = 'TP. Hồ Chí Minh';
            $lat = 10.8231;
            $lon = 106.6297;
        } elseif (str_contains($query, 'đà nẵng') || str_contains($query, 'da nang')) {
            $city = 'Đà Nẵng';
            $lat = 16.0544;
            $lon = 108.2022;
        } elseif (str_contains($query, 'hải phòng')) {
            $city = 'Hải Phòng';
            $lat = 20.8449;
            $lon = 106.6881;
        } elseif (str_contains($query, 'cần thơ')) {
            $city = 'Cần Thơ';
            $lat = 10.0452;
            $lon = 105.7469;
        }

        return Cache::remember('weather_' . md5($city), 600, function () use ($city, $lat, $lon) {
            try {
                $res = Http::withoutVerifying()
                    ->timeout(3)
                    ->get("https://api.open-meteo.com/v1/forecast", [
                        'latitude' => $lat,
                        'longitude' => $lon,
                        'current' => 'temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,rain,weather_code,wind_speed_10m',
                        'timezone' => 'Asia/Bangkok',
                    ]);

                if ($res->successful()) {
                    $cur = $res->json('current') ?? [];
                    $temp = $cur['temperature_2m'] ?? null;
                    $humidity = $cur['relative_humidity_2m'] ?? null;
                    $rain = $cur['precipitation'] ?? 0;
                    $wind = $cur['wind_speed_10m'] ?? null;

                    $rainDesc = ($rain > 0) ? "Có mưa (lượng mưa {$rain}mm)" : "Hiện tại không mưa";
                    return "- Thành phố: {$city}\n"
                        . "- Nhiệt độ hiện tại: {$temp}°C (Cảm giác như: " . ($cur['apparent_temperature'] ?? $temp) . "°C)\n"
                        . "- Độ ẩm không khí: {$humidity}%\n"
                        . "- Tình trạng mưa: {$rainDesc}\n"
                        . "- Tốc độ gió: {$wind} km/h";
                }
            } catch (Throwable $e) {}

            return "- Thành phố: {$city}\n- Nhiệt độ trung bình hôm nay: 26°C - 30°C, thời tiết thuận lợi cho các hoạt động thể thao.";
        });
    }

    /**
     * Phản hồi dự phòng thông minh khi Gemini API tạm thời bận hoặc không có kết nối internet
     */
    protected function fallbackReply(int $userId, string $message, string $context, bool $hasImage = false): string
    {
        if ($hasImage) {
            return "Mình đã nhận được hình ảnh giày đá bóng bạn gửi! 📸✨\n\n"
                . "Qua hình ảnh, đây là mẫu giày bóng đá chính hãng với thiết kế hiện đại, hỗ trợ kiểm soát bóng và bứt tốc tuyệt vời. STRIKER có sẵn các dòng giày tương tự (Nike Mercurial, Adidas Predator, Puma Future) với đầy đủ đinh TF/FG cho sân cỏ nhân tạo & tự nhiên.\n\n"
                . "Bạn có muốn shop tư vấn thêm về size giày hoặc gửi thêm hình ảnh cận cảnh để kiểm tra chi tiết không ạ? ⚽👟";
        }

        $normalized = mb_strtolower(trim($message), 'UTF-8');

        // 1. Phép toán (ví dụ: 1+1 = 2)
        if (preg_match('/^(\d+)\s*([\+\-\*\/xX])\s*(\d+)/', $normalized, $matches)) {
            $num1 = (float)$matches[1];
            $op = $matches[2];
            $num2 = (float)$matches[3];
            $res = match ($op) {
                '+' => $num1 + $num2,
                '-' => $num1 - $num2,
                '*', 'x', 'X' => $num1 * $num2,
                '/' => $num2 != 0 ? round($num1 / $num2, 2) : 'không thể chia cho 0',
                default => null,
            };
            if ($res !== null) {
                return "Kết quả của {$num1} {$op} {$num2} = {$res} bạn nhé! ✨ Bạn cần mình hỗ trợ thêm gì nữa không?";
            }
        }

        // 2. Tra cứu đơn hàng
        if (str_contains($normalized, 'đơn hàng') || str_contains($normalized, 'đơn của tôi') || str_contains($normalized, 'kiểm tra đơn') || str_contains($normalized, 'tra cứu đơn')) {
            return "Dưới đây là thẻ trạng thái tiến trình giao hàng chi tiết cho đơn hàng của bạn! Bạn có thể theo dõi trực tiếp các mốc vận chuyển của đơn vị GHN ngay trên thẻ nhé. 📦🚚";
        }

        // 3. Thời tiết thời gian thực
        if (str_contains($normalized, 'thời tiết') || str_contains($normalized, 'mưa không') || str_contains($normalized, 'trời hôm nay')) {
            $weather = $this->fetchRealtimeWeather($normalized);
            if (!empty($weather)) {
                return "Dữ liệu thời tiết hiện tại:\n{$weather}\n\nThời tiết này rất tuyệt vời để bạn ra sân đá bóng hoặc vận động thể thao nhé! ⚽";
            }
            return "Thời tiết hôm nay khá đẹp và mát mẻ, rất thích hợp để mang giày ra sân bóng đấy bạn ơi! ⚽";
        }

        // 4. Địa chỉ showroom
        if (str_contains($normalized, 'cửa hàng') || str_contains($normalized, 'shop ở đâu') || str_contains($normalized, 'địa chỉ')) {
            return "Showroom STRIKER hiện có 2 chi nhánh chính thức:\n"
                . "📍 Hà Nội: 123 Đường Cầu Giấy, Quận Cầu Giấy\n"
                . "📍 TP.HCM: 456 Đường Lê Văn Sỹ, Quận 3\n"
                . "Mời bạn ghé shop để thử size giày trực tiếp ạ!";
        }

        // 5. Voucher khuyến mãi
        if (str_contains($normalized, 'voucher') || str_contains($normalized, 'mã giảm giá') || str_contains($normalized, 'khuyến mãi')) {
            return "Hiện tại STRIKER đang có các ưu đãi cực hot:\n"
                . "🎟️ FREESHIP: Miễn phí vận chuyển toàn quốc\n"
                . "🎟️ STRIKER10: Giảm 10% cho đơn hàng tiếp theo\n"
                . "🎟️ WELCOME20: Giảm 20.000đ cho thành viên mới\n"
                . "Bạn có thể áp dụng trực tiếp tại bước thanh toán giỏ hàng nhé!";
        }

        // 6. Tư vấn size giày
        if (str_contains($normalized, 'size') || str_contains($normalized, 'chân')) {
            return "Hướng dẫn chọn size giày bóng đá tại STRIKER:\n"
                . "1. Đo chiều dài bàn chân từ gót đến ngón dài nhất (cm).\n"
                . "2. Nếu chân thon, bạn chọn đúng size cm. Nếu chân bè ngang, bạn nên tăng thêm 0.5 đến 1 size.\n"
                . "STRIKER hỗ trợ đổi size miễn phí trong 30 ngày nếu bạn mang chưa vừa vặn ạ!";
        }

        return "Chào bạn! Mình là trợ lý AI của STRIKER ⚽. Mình có thể giúp bạn tư vấn các mẫu giày bóng đá chính hãng, nhận diện mẫu giày qua hình ảnh, tra cứu đơn hàng hoặc giải đáp mọi câu hỏi khác. Bạn cần mình hỗ trợ gì ạ?";
    }
}
