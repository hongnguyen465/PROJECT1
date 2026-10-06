<?php

namespace Database\Seeders;

use App\Models\User;
use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\Hash;

class DatabaseSeeder extends Seeder
{
    public function run(): void
    {
        // 1. Seed Users (Admin + Customers)
        User::updateOrCreate(
            ['email' => 'admin@striker.vn'],
            [
                'name' => 'Quản Trị Viên Striker',
                'email_verified_at' => now(),
                'password' => Hash::make('123456'),
                'phone' => '0909999999',
                'role' => 'admin',
                'is_active' => true,
            ]
        );

        User::updateOrCreate(
            ['email' => 'user@striker.vn'],
            [
                'name' => 'Người Dùng Striker',
                'email_verified_at' => now(),
                'password' => Hash::make('123456'),
                'phone' => '0911111111',
                'role' => 'customer',
                'is_active' => true,
            ]
        );

        User::updateOrCreate(
            ['email' => 'customer@striker.vn'],
            [
                'name' => 'Nguyễn Văn An',
                'email_verified_at' => now(),
                'password' => Hash::make('123456'),
                'phone' => '0977777777',
                'role' => 'customer',
                'is_active' => true,
            ]
        );

        User::updateOrCreate(
            ['email' => 'hoang.tran@gmail.com'],
            [
                'name' => 'Trần Minh Hoàng',
                'email_verified_at' => now(),
                'password' => Hash::make('123456'),
                'phone' => '0988776655',
                'role' => 'customer',
                'is_active' => true,
            ]
        );

        User::updateOrCreate(
            ['email' => 'baole.striker@gmail.com'],
            [
                'name' => 'Lê Quốc Bảo',
                'email_verified_at' => now(),
                'password' => Hash::make('123456'),
                'phone' => '0912345678',
                'role' => 'customer',
                'is_active' => true,
            ]
        );

        User::updateOrCreate(
            ['email' => 'huong.pham@gmail.com'],
            [
                'name' => 'Phạm Thu Hương',
                'email_verified_at' => now(),
                'password' => Hash::make('123456'),
                'phone' => '0903332211',
                'role' => 'customer',
                'is_active' => true,
            ]
        );

        // 2. Seed Catalog (Categories, Brands, Products, Banners)
        $this->call([
            CategorySeeder::class,
            BrandSeeder::class,
            ProductSeeder::class,
            BannerSeeder::class,
            CouponSeeder::class,
            OrderSeeder::class,
            ReviewSeeder::class,
        ]);
    }
}
