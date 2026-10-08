<?php

namespace Database\Seeders;

use App\Models\User;
use Illuminate\Database\Seeder;

class DatabaseSeeder extends Seeder
{
    public function run(): void
    {
        // 1. Admin
        User::updateOrCreate(
            ['id' => 1],
            [
                'name' => 'Quản Trị Viên Striker',
                'email' => 'admin@striker.vn',
                'password' => 'password',
                'phone' => '0909999999',
                'role' => 'admin',
                'is_active' => true,
                'email_verified_at' => now(),
            ]
        );

        // 2. Customer 1 - Nguyễn Văn An
        User::updateOrCreate(
            ['id' => 2],
            [
                'name' => 'Nguyễn Văn An',
                'email' => 'customer@striker.vn',
                'password' => 'password',
                'phone' => '0977777777',
                'role' => 'customer',
                'is_active' => true,
                'email_verified_at' => now(),
            ]
        );

        // 3. Customer 2 - Trần Minh Hoàng
        User::updateOrCreate(
            ['id' => 3],
            [
                'name' => 'Trần Minh Hoàng',
                'email' => 'hoang.tran@gmail.com',
                'password' => 'password',
                'phone' => '0988776655',
                'role' => 'customer',
                'is_active' => true,
                'email_verified_at' => now(),
            ]
        );

        // 4. Customer 3 - Lê Quốc Bảo
        User::updateOrCreate(
            ['id' => 4],
            [
                'name' => 'Lê Quốc Bảo',
                'email' => 'baole.striker@gmail.com',
                'password' => 'password',
                'phone' => '0912345678',
                'role' => 'customer',
                'is_active' => true,
                'email_verified_at' => now(),
            ]
        );

        // 5. Customer 4 - Phạm Thu Hương
        User::updateOrCreate(
            ['id' => 5],
            [
                'name' => 'Phạm Thu Hương',
                'email' => 'huong.pham@gmail.com',
                'password' => 'password',
                'phone' => '0903332211',
                'role' => 'customer',
                'is_active' => true,
                'email_verified_at' => now(),
            ]
        );

        // 6. User - Người Dùng Striker
        User::updateOrCreate(
            ['id' => 6],
            [
                'name' => 'Người Dùng Striker',
                'email' => 'user@striker.vn',
                'password' => 'password',
                'phone' => '0911111111',
                'role' => 'customer',
                'is_active' => true,
                'email_verified_at' => now(),
            ]
        );
    }
}
