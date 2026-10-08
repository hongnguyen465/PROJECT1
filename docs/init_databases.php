<?php
// Auto Initialize Databases & Check MySQL Connection

$services = ['auth-service', 'catalog-service', 'order-service', 'payment-service', 'chat-service'];
$defaultDbs = [
    'auth-service' => 'football_auth_db',
    'catalog-service' => 'football_catalog_db',
    'order-service' => 'football_order_db',
    'payment-service' => 'football_payment_db',
    'chat-service' => 'football_chat_db',
];

foreach ($services as $svc) {
    $envFile = __DIR__ . "/../{$svc}/.env";
    $host = '127.0.0.1';
    $port = 3306;
    $user = 'root';
    $pass = '';
    $dbName = $defaultDbs[$svc] ?? '';

    if (file_exists($envFile)) {
        $lines = file($envFile, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
        foreach ($lines as $line) {
            $line = trim($line);
            if (str_starts_with($line, '#')) continue;
            if (str_contains($line, '=')) {
                [$k, $v] = explode('=', $line, 2);
                $k = trim($k);
                $v = trim($v, " \t\n\r\0\x0B\"'");
                if ($k === 'DB_HOST') $host = $v;
                if ($k === 'DB_PORT') $port = (int)$v;
                if ($k === 'DB_USERNAME') $user = $v;
                if ($k === 'DB_PASSWORD') $pass = $v;
                if ($k === 'DB_DATABASE') $dbName = $v;
            }
        }
    }

    if (!empty($dbName)) {
        try {
            $pdo = new PDO("mysql:host={$host};port={$port}", $user, $pass, [
                PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
                PDO::ATTR_TIMEOUT => 2,
            ]);
            $pdo->exec("CREATE DATABASE IF NOT EXISTS `{$dbName}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;");
            echo " [DB OK] {$dbName}\n";
        } catch (Throwable $e) {
            echo " [DB Note] {$dbName}: " . $e->getMessage() . "\n";
        }
    }
}
