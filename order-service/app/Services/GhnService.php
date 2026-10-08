<?php

namespace App\Services;

use App\Models\Order;
use Exception;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\Log;

class GhnService
{
    protected string $token;
    protected int $shopId;
    protected string $baseUrl;
    protected int $fromDistrictId;

    public function __construct()
    {
        $this->token = (string) config('services.ghn.token', env('GHN_TOKEN', '84d13de2-aa85-11f1-a973-aee5264794df'));
        $this->shopId = (int) config('services.ghn.shop_id', env('GHN_SHOP_ID', 217482));
        $this->baseUrl = rtrim((string) config('services.ghn.base_url', env('GHN_BASE_URL', 'https://dev-online-gateway.ghn.vn/shiip/public-api')), '/');
        $this->fromDistrictId = (int) config('services.ghn.from_district_id', env('GHN_FROM_DISTRICT_ID', 1482));
    }

    /**
     * Execute direct cURL request to GHN API with SSL bypass and fast timeout.
     */
    protected function requestGhn(string $path, string $method = 'GET', array $data = [], ?int $customTimeout = 3, bool $withShopId = false): ?array
    {
        $url = $this->baseUrl . '/' . ltrim($path, '/');

        if (strtoupper($method) === 'GET' && !empty($data)) {
            $url .= (strpos($url, '?') === false ? '?' : '&') . http_build_query($data);
        }

        $ch = curl_init($url);

        $headers = [
            'Token: ' . $this->token,
            'token: ' . $this->token,
            'Content-Type: application/json',
        ];

        if ($withShopId && $this->shopId > 0) {
            $headers[] = 'ShopId: ' . $this->shopId;
            $headers[] = 'shop_id: ' . $this->shopId;
        }

        $opts = [
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_SSL_VERIFYPEER => false,
            CURLOPT_SSL_VERIFYHOST => false,
            CURLOPT_TIMEOUT => $customTimeout ?? 3,
            CURLOPT_CONNECTTIMEOUT => 2,
            CURLOPT_HTTPHEADER => $headers,
        ];

        if (strtoupper($method) === 'POST') {
            $opts[CURLOPT_POST] = true;
            $opts[CURLOPT_POSTFIELDS] = json_encode($data);
        }

        curl_setopt_array($ch, $opts);
        $response = curl_exec($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        $err = curl_error($ch);
        curl_close($ch);

        if ($err) {
            Log::warning("GHN direct cURL error on [{$path}]: {$err}");
            return null;
        }

        if ($httpCode < 200 || $httpCode >= 300) {
            Log::warning("GHN direct cURL returned HTTP {$httpCode} on [{$path}]", ['res' => substr((string)$response, 0, 200)]);
            return null;
        }

        $decoded = json_decode((string) $response, true);
        return is_array($decoded) ? $decoded : null;
    }

    /**
     * Get list of all provinces/cities in Vietnam (instant local file + GHN fallback).
     */
    public function getProvinces(): array
    {
        return Cache::remember('ghn_provinces_v6', 86400, function () {
            // 1. Check local pre-dumped dataset (65 provinces)
            $localFile = storage_path('app/all_provinces.json');
            if (file_exists($localFile)) {
                $raw = @file_get_contents($localFile);
                $json = json_decode((string) $raw, true);
                if (!empty($json['data']) && is_array($json['data'])) {
                    return collect($json['data'])
                        ->filter(fn ($p) => ($p['Status'] ?? 1) === 1 && !empty($p['ProvinceName']))
                        ->values()
                        ->all();
                }
            }

            // 2. Direct GHN request
            $res = $this->requestGhn('master-data/province', 'GET', [], 3, false);
            if (!empty($res['data']) && is_array($res['data'])) {
                return collect($res['data'])
                    ->filter(fn ($p) => ($p['Status'] ?? 1) === 1 && !empty($p['ProvinceName']))
                    ->values()
                    ->all();
            }

            return $this->getFallbackProvinces();
        });
    }

    /**
     * Get list of districts by province ID (instant local file + GHN fallback).
     */
    public function getDistricts(int $provinceId): array
    {
        if ($provinceId <= 0) {
            return [];
        }

        return Cache::remember("ghn_districts_{$provinceId}_v6", 86400, function () use ($provinceId) {
            // 1. Check local pre-dumped dataset (727 districts across Vietnam)
            $localFile = storage_path('app/all_districts.json');
            if (file_exists($localFile)) {
                $raw = @file_get_contents($localFile);
                $json = json_decode((string) $raw, true);
                if (!empty($json['data']) && is_array($json['data'])) {
                    $matched = collect($json['data'])
                        ->filter(fn ($d) => (int) ($d['ProvinceID'] ?? 0) === $provinceId && ($d['Status'] ?? 1) === 1)
                        ->values()
                        ->all();

                    if (!empty($matched)) {
                        return $matched;
                    }
                }
            }

            // 2. Direct GHN request
            $res = $this->requestGhn('master-data/district', 'POST', [
                'province_id' => $provinceId,
            ], 3, false);

            if (!empty($res['data']) && is_array($res['data'])) {
                return $res['data'];
            }

            return [];
        });
    }

    /**
     * Get list of wards by district ID (local disk cache + GHN request + fallback).
     */
    public function getWards(int $districtId): array
    {
        if ($districtId <= 0) {
            return [];
        }

        return Cache::remember("ghn_wards_{$districtId}_v6", 86400, function () use ($districtId) {
            $wardDir = storage_path('app/ghn_wards');
            if (!is_dir($wardDir)) {
                @mkdir($wardDir, 0777, true);
            }

            $wardFile = "{$wardDir}/{$districtId}.json";
            if (file_exists($wardFile)) {
                $raw = @file_get_contents($wardFile);
                $json = json_decode((string) $raw, true);
                if (!empty($json) && is_array($json)) {
                    return $json;
                }
            }

            // Direct GHN request with 2s timeout
            $res = $this->requestGhn('master-data/ward', 'GET', [
                'district_id' => $districtId,
            ], 2, false);

            if (!empty($res['data']) && is_array($res['data'])) {
                @file_put_contents($wardFile, json_encode($res['data'], JSON_UNESCAPED_UNICODE));
                return $res['data'];
            }

            $postRes = $this->requestGhn('master-data/ward', 'POST', [
                'district_id' => $districtId,
            ], 2, false);

            if (!empty($postRes['data']) && is_array($postRes['data'])) {
                @file_put_contents($wardFile, json_encode($postRes['data'], JSON_UNESCAPED_UNICODE));
                return $postRes['data'];
            }

            $fallback = $this->getFallbackWards($districtId);
            @file_put_contents($wardFile, json_encode($fallback, JSON_UNESCAPED_UNICODE));
            return $fallback;
        });
    }

    /**
     * Fallback wards generator for any district ID.
     */
    public function getFallbackWards(int $districtId): array
    {
        return [
            ['WardCode' => "{$districtId}01", 'DistrictID' => $districtId, 'WardName' => 'Phường Trung Tâm'],
            ['WardCode' => "{$districtId}02", 'DistrictID' => $districtId, 'WardName' => 'Phường 1'],
            ['WardCode' => "{$districtId}03", 'DistrictID' => $districtId, 'WardName' => 'Phường 2'],
            ['WardCode' => "{$districtId}04", 'DistrictID' => $districtId, 'WardName' => 'Phường 3'],
            ['WardCode' => "{$districtId}05", 'DistrictID' => $districtId, 'WardName' => 'Phường 4'],
            ['WardCode' => "{$districtId}06", 'DistrictID' => $districtId, 'WardName' => 'Phường 5'],
            ['WardCode' => "{$districtId}07", 'DistrictID' => $districtId, 'WardName' => 'Xã 1'],
            ['WardCode' => "{$districtId}08", 'DistrictID' => $districtId, 'WardName' => 'Xã 2'],
        ];
    }

    /**
     * Calculate shipping fee based on destination district and ward.
     */
    public function calculateFee(
        int $toDistrictId,
        string $toWardCode,
        int $weight = 500,
        int $length = 20,
        int $width = 15,
        int $height = 10,
        int $insuranceValue = 0
    ): array {
        $payload = [
            'from_district_id' => $this->fromDistrictId,
            'to_district_id' => $toDistrictId,
            'to_ward_code' => (string) $toWardCode,
            'service_type_id' => 2, // Giao hàng chuẩn
            'weight' => max(100, $weight),
            'length' => max(5, $length),
            'width' => max(5, $width),
            'height' => max(5, $height),
            'insurance_value' => max(0, $insuranceValue),
        ];

        $res = $this->requestGhn('v2/shipping-order/fee', 'POST', $payload, 3, true);
        if (!empty($res['data']['total'])) {
            return $res['data'];
        }

        $fee = ($toDistrictId === $this->fromDistrictId) ? 22000 : 35000;
        return [
            'total' => $fee,
            'service_fee' => $fee,
            'insurance_fee' => 0,
            'pick_station_fee' => 0,
            'coupon_value' => 0,
            'r2s_fee' => 0,
        ];
    }

    /**
     * Create real shipping order on GHN Sandbox / Production API.
     */
    public function createShippingOrder(Order $order, array $customData = []): array
    {
        $order->loadMissing('items');

        $items = $order->items->map(fn ($item) => [
            'name' => $item->product_name ?? 'Sản phẩm thể thao',
            'code' => $item->sku ?? 'SP-'.$item->product_id,
            'quantity' => (int) $item->quantity,
            'price' => (int) $item->price,
            'weight' => 300,
        ])->toArray();

        if (empty($items)) {
            $items = [[
                'name' => 'Gói hàng thể thao Striker',
                'quantity' => 1,
                'price' => (int) $order->total_amount,
                'weight' => 300,
            ]];
        }

        $totalWeight = max(300, (int) ($customData['weight'] ?? $order->items->sum(fn ($i) => ((int) ($i->quantity ?: 1)) * 300)));

        $toDistrictId = !empty($customData['to_district_id'])
            ? (int) $customData['to_district_id']
            : (!empty($order->to_district_id) ? (int) $order->to_district_id : 1442);

        $toWardCode = !empty($customData['to_ward_code'])
            ? (string) $customData['to_ward_code']
            : (!empty($order->to_ward_code) ? (string) $order->to_ward_code : '20110');

        $payload = [
            'shop_id' => $this->shopId,
            'client_order_code' => $order->order_number ?: ($order->order_code ?: ('ORD-' . $order->id)),
            'payment_type_id' => 1, // 1: Shop trả phí cước vận chuyển
            'note' => $customData['note'] ?? $order->note ?? 'Hàng giá trị cao, vui lòng cho xem và thử hàng.',
            'required_note' => $customData['required_note'] ?? 'CHOTHUHANG',
            'from_name' => 'CRS Cyber-Sport Store',
            'from_phone' => '0345155356',
            'from_address' => '41A Phú Diễn, Phường Phú Diễn, Quận Bắc Từ Liêm, Hà Nội',
            'from_district_id' => $this->fromDistrictId,
            'return_phone' => '0345155356',
            'return_address' => '41A Phú Diễn, Phường Phú Diễn, Quận Bắc Từ Liêm, Hà Nội',
            'return_district_id' => $this->fromDistrictId,
            'to_name' => $order->shipping_name ?: 'Khách hàng',
            'to_phone' => $order->phone ?: $order->shipping_phone ?: '0901234567',
            'to_address' => $order->shipping_address ?: '123 Lê Lợi, Phường Tân Định, Quận 1, TP Hồ Chí Minh',
            'to_district_id' => $toDistrictId,
            'to_ward_code' => $toWardCode,
            'cod_amount' => ($order->payment_method === 'cod') ? (int) $order->total_amount : 0,
            'content' => 'Đơn hàng thể thao #'.$order->order_number,
            'weight' => $totalWeight,
            'length' => (int) ($customData['length'] ?? 20),
            'width' => (int) ($customData['width'] ?? 15),
            'height' => (int) ($customData['height'] ?? 10),
            'insurance_value' => 0,
            'service_type_id' => 2,
            'items' => $items,
        ];

        $res = $this->requestGhn('v2/shipping-order/create', 'POST', $payload, 8, true);
        if (!empty($res['data'])) {
            return $res['data'];
        }

        $msg = $res['message'] ?? $res['code_message_value'] ?? 'Không thể tạo đơn giao hàng qua GHN Sandbox.';
        throw new Exception($msg);
    }

    /**
     * Fallback list of provinces with real GHN IDs.
     */
    public function getFallbackProvinces(): array
    {
        return [
            ['ProvinceID' => 201, 'ProvinceName' => 'Hà Nội', 'Code' => '4'],
            ['ProvinceID' => 202, 'ProvinceName' => 'Hồ Chí Minh', 'Code' => '8'],
            ['ProvinceID' => 203, 'ProvinceName' => 'Đà Nẵng', 'Code' => '511'],
            ['ProvinceID' => 204, 'ProvinceName' => 'Đồng Nai', 'Code' => '61'],
            ['ProvinceID' => 205, 'ProvinceName' => 'Bình Dương', 'Code' => '650'],
            ['ProvinceID' => 206, 'ProvinceName' => 'Bà Rịa - Vũng Tàu', 'Code' => '64'],
            ['ProvinceID' => 207, 'ProvinceName' => 'Gia Lai', 'Code' => '59'],
            ['ProvinceID' => 208, 'ProvinceName' => 'Khánh Hòa', 'Code' => '58'],
            ['ProvinceID' => 209, 'ProvinceName' => 'Lâm Đồng', 'Code' => '63'],
            ['ProvinceID' => 210, 'ProvinceName' => 'Đắk Lắk', 'Code' => '500'],
            ['ProvinceID' => 211, 'ProvinceName' => 'Long An', 'Code' => '72'],
            ['ProvinceID' => 212, 'ProvinceName' => 'Tiền Giang', 'Code' => '73'],
            ['ProvinceID' => 213, 'ProvinceName' => 'Bến Tre', 'Code' => '75'],
            ['ProvinceID' => 214, 'ProvinceName' => 'Trà Vinh', 'Code' => '74'],
            ['ProvinceID' => 215, 'ProvinceName' => 'Vĩnh Long', 'Code' => '70'],
            ['ProvinceID' => 216, 'ProvinceName' => 'Đồng Tháp', 'Code' => '67'],
            ['ProvinceID' => 217, 'ProvinceName' => 'An Giang', 'Code' => '76'],
            ['ProvinceID' => 218, 'ProvinceName' => 'Sóc Trăng', 'Code' => '79'],
            ['ProvinceID' => 219, 'ProvinceName' => 'Kiên Giang', 'Code' => '77'],
            ['ProvinceID' => 220, 'ProvinceName' => 'Cần Thơ', 'Code' => '710'],
            ['ProvinceID' => 221, 'ProvinceName' => 'Vĩnh Phúc', 'Code' => '211'],
            ['ProvinceID' => 223, 'ProvinceName' => 'Thừa Thiên Huế', 'Code' => '54'],
            ['ProvinceID' => 224, 'ProvinceName' => 'Hải Phòng', 'Code' => '31'],
            ['ProvinceID' => 225, 'ProvinceName' => 'Hải Dương', 'Code' => '320'],
            ['ProvinceID' => 226, 'ProvinceName' => 'Thái Bình', 'Code' => '36'],
            ['ProvinceID' => 227, 'ProvinceName' => 'Hà Giang', 'Code' => '219'],
            ['ProvinceID' => 228, 'ProvinceName' => 'Tuyên Quang', 'Code' => '27'],
            ['ProvinceID' => 229, 'ProvinceName' => 'Phú Thọ', 'Code' => '210'],
            ['ProvinceID' => 230, 'ProvinceName' => 'Quảng Ninh', 'Code' => '33'],
            ['ProvinceID' => 231, 'ProvinceName' => 'Nam Định', 'Code' => '350'],
            ['ProvinceID' => 232, 'ProvinceName' => 'Hà Nam', 'Code' => '351'],
            ['ProvinceID' => 233, 'ProvinceName' => 'Ninh Bình', 'Code' => '30'],
            ['ProvinceID' => 234, 'ProvinceName' => 'Thanh Hóa', 'Code' => '37'],
            ['ProvinceID' => 235, 'ProvinceName' => 'Nghệ An', 'Code' => '38'],
            ['ProvinceID' => 236, 'ProvinceName' => 'Hà Tĩnh', 'Code' => '39'],
            ['ProvinceID' => 237, 'ProvinceName' => 'Quảng Bình', 'Code' => '52'],
            ['ProvinceID' => 238, 'ProvinceName' => 'Quảng Trị', 'Code' => '53'],
            ['ProvinceID' => 239, 'ProvinceName' => 'Bình Phước', 'Code' => '651'],
            ['ProvinceID' => 240, 'ProvinceName' => 'Tây Ninh', 'Code' => '66'],
            ['ProvinceID' => 241, 'ProvinceName' => 'Đắk Nông', 'Code' => '501'],
            ['ProvinceID' => 242, 'ProvinceName' => 'Quảng Ngãi', 'Code' => '55'],
            ['ProvinceID' => 243, 'ProvinceName' => 'Quảng Nam', 'Code' => '510'],
            ['ProvinceID' => 244, 'ProvinceName' => 'Thái Nguyên', 'Code' => '280'],
            ['ProvinceID' => 245, 'ProvinceName' => 'Bắc Kạn', 'Code' => '281'],
            ['ProvinceID' => 246, 'ProvinceName' => 'Cao Bằng', 'Code' => '26'],
            ['ProvinceID' => 247, 'ProvinceName' => 'Lạng Sơn', 'Code' => '25'],
            ['ProvinceID' => 248, 'ProvinceName' => 'Bắc Giang', 'Code' => '240'],
            ['ProvinceID' => 249, 'ProvinceName' => 'Bắc Ninh', 'Code' => '241'],
            ['ProvinceID' => 250, 'ProvinceName' => 'Hậu Giang', 'Code' => '711'],
            ['ProvinceID' => 252, 'ProvinceName' => 'Cà Mau', 'Code' => '780'],
            ['ProvinceID' => 253, 'ProvinceName' => 'Bạc Liêu', 'Code' => '781'],
            ['ProvinceID' => 258, 'ProvinceName' => 'Bình Thuận', 'Code' => '62'],
            ['ProvinceID' => 259, 'ProvinceName' => 'Kon Tum', 'Code' => '60'],
            ['ProvinceID' => 260, 'ProvinceName' => 'Phú Yên', 'Code' => '57'],
            ['ProvinceID' => 261, 'ProvinceName' => 'Ninh Thuận', 'Code' => '68'],
            ['ProvinceID' => 262, 'ProvinceName' => 'Bình Định', 'Code' => '56'],
            ['ProvinceID' => 263, 'ProvinceName' => 'Yên Bái', 'Code' => '29'],
            ['ProvinceID' => 264, 'ProvinceName' => 'Lai Châu', 'Code' => '231'],
            ['ProvinceID' => 265, 'ProvinceName' => 'Điện Biên', 'Code' => '230'],
            ['ProvinceID' => 266, 'ProvinceName' => 'Sơn La', 'Code' => '22'],
            ['ProvinceID' => 267, 'ProvinceName' => 'Hòa Bình', 'Code' => '218'],
            ['ProvinceID' => 268, 'ProvinceName' => 'Hưng Yên', 'Code' => '321'],
            ['ProvinceID' => 269, 'ProvinceName' => 'Lào Cai', 'Code' => '20'],
        ];
    }
}
