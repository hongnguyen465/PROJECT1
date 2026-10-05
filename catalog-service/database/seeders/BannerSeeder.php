<?php

namespace Database\Seeders;

use App\Models\Banner;
use Illuminate\Database\Seeder;

class BannerSeeder extends Seeder
{
    public function run(): void
    {
        Banner::truncate();

        $banners = [
            [
                'title' => 'Play forward.',
                'subtitle' => 'NEW SEASON / 2026 ELITE PACK',
                'tag' => 'BỘ SƯU TẬP MỚI',
                'image' => 'https://images.unsplash.com/photo-1579952363873-27f3bade9f55?auto=format&fit=crop&w=2200&q=90',
                'link' => '/shop?category=giay-bong-da',
                'order' => 1,
                'is_active' => true,
            ],
            [
                'title' => 'Speed reimagined.',
                'subtitle' => 'MERCURIAL & F50 PRO EDITIONS',
                'tag' => 'TỐC ĐỘ BỨT PHÁ',
                'image' => 'https://images.unsplash.com/photo-1511886929837-354d827aae26?auto=format&fit=crop&w=2200&q=90',
                'link' => '/shop?category=giay-bong-da',
                'order' => 2,
                'is_active' => true,
            ],
            [
                'title' => 'Match ready.',
                'subtitle' => 'FIFA QUALITY PRO BALLS',
                'tag' => 'BÓNG THI ĐẤU CHÍNH HÃNG',
                'image' => 'https://images.unsplash.com/photo-1552674605-db6ffd4facb5?auto=format&fit=crop&w=2200&q=90',
                'link' => '/shop?category=bong-thi-dau',
                'order' => 3,
                'is_active' => true,
            ],
            [
                'title' => 'Born for glory.',
                'subtitle' => 'AUTHENTIC KITS 2025/2026',
                'tag' => 'ÁO ĐẤU CÂU LẠC BỘ',
                'image' => 'https://images.unsplash.com/photo-1517466787929-bc90951d0974?auto=format&fit=crop&w=2200&q=90',
                'link' => '/shop?category=ao-dau',
                'order' => 4,
                'is_active' => true,
            ],
            [
                'title' => 'Pro defense gear.',
                'subtitle' => 'ELITE GLOVES & GUARDS',
                'tag' => 'PHỤ KIỆN BÓNG ĐÁ',
                'image' => 'https://images.unsplash.com/photo-1508098682722-e99c43a406b2?auto=format&fit=crop&w=2200&q=90',
                'link' => '/shop?category=phu-kien',
                'order' => 5,
                'is_active' => true,
            ],
            [
                'title' => 'Own the pitch.',
                'subtitle' => 'CHÍNH HÃNG 100% • GIAO SIÊU TỐC',
                'tag' => 'ƯU ĐÃI ĐỘC QUYỀN',
                'image' => 'https://images.unsplash.com/photo-1574629810360-7efbbe195018?auto=format&fit=crop&w=2200&q=90',
                'link' => '/shop',
                'order' => 6,
                'is_active' => true,
            ],
        ];

        foreach ($banners as $b) {
            Banner::create($b);
        }
    }
}
