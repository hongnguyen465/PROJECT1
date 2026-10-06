<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration {
    public function up(): void
    {
        if (Schema::hasTable('cart_items') && !Schema::hasColumn('cart_items', 'price')) {
            Schema::table('cart_items', function (Blueprint $table) {
                $table->decimal('price', 12, 2)->default(0)->after('quantity');
            });
        }
    }

    public function down(): void
    {
        if (Schema::hasTable('cart_items') && Schema::hasColumn('cart_items', 'price')) {
            Schema::table('cart_items', function (Blueprint $table) {
                $table->dropColumn('price');
            });
        }
    }
};
