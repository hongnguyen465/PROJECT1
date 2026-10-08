# ========================================================
# STRIKER E-COMMERCE MICROSERVICES STARTUP SCRIPT
# ========================================================

Write-Host "`n>>> Kiem tra va giai phong cac cong mang (8000-8005, 5173)..." -ForegroundColor Cyan
$ports = @(8000, 8001, 8002, 8003, 8004, 8005, 5173)
foreach ($port in $ports) {
    $connections = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
    if ($connections) {
        foreach ($conn in $connections) {
            if ($conn.OwningProcess -gt 0) {
                Stop-Process -Id $conn.OwningProcess -Force -ErrorAction SilentlyContinue
            }
        }
    }
}

Start-Sleep -Milliseconds 500

# Tu dong kiem tra va khoi tao dependencies / file .env neu thieu
$services = @("api-gateway", "auth-service", "catalog-service", "order-service", "payment-service", "chat-service")
foreach ($svc in $services) {
    if (Test-Path $svc) {
        # 1. Tao .env neu chua co
        if (-not (Test-Path "$svc/.env")) {
            if (Test-Path "$svc/.env.example") {
                Write-Host ">>> [Auto-Setup] Tao file .env cho $svc tu .env.example..." -ForegroundColor Yellow
                Copy-Item "$svc/.env.example" "$svc/.env"
            }
        }
        
        # 2. Chay composer install neu chua co vendor
        if (-not (Test-Path "$svc/vendor/autoload.php")) {
            Write-Host ">>> [Auto-Setup] Dang tu dong cai dat vendor (composer install) cho $svc..." -ForegroundColor Green
            Push-Location $svc
            composer install --no-interaction
            php artisan key:generate --force
            Pop-Location
        }
    }
}

# 3. Tu dong khoi tao database MySQL va chay migration neu can
Write-Host "`n>>> [Auto-Setup] Kiem tra co so du lieu MySQL va chay Migration cho cac Microservices..." -ForegroundColor Yellow
if (Test-Path "docs/init_databases.php") {
    php docs/init_databases.php
}

$dbServices = @("auth-service", "catalog-service", "order-service", "payment-service", "chat-service")
foreach ($svc in $dbServices) {
    if (Test-Path "$svc/artisan") {
        Push-Location $svc
        php artisan migrate --force --no-interaction | Out-Null
        Pop-Location
    }
}

# 4. Chay npm install cho frontend neu chua co node_modules
if (-not (Test-Path "crs-frontend/node_modules")) {
    Write-Host ">>> [Auto-Setup] Dang tu dong cai dat node_modules (npm install) cho crs-frontend..." -ForegroundColor Green
    Push-Location "crs-frontend"
    npm install
    Pop-Location
}

$env:PHP_CLI_SERVER_WORKERS = "8"

Write-Host "`n>>> Dang khoi dong toan bo he thong Microservices & Frontend..." -ForegroundColor Cyan

npx -y concurrently -n "GATEWAY,AUTH,CATALOG,ORDER,PAY,CHAT,FRONTEND" `
  -c "blue,magenta,yellow,cyan,blue,red,green" `
  "cd api-gateway && php artisan serve --port=8000" `
  "cd auth-service && php artisan serve --port=8001" `
  "cd catalog-service && php artisan serve --port=8002" `
  "cd order-service && php artisan serve --port=8003" `
  "cd payment-service && php artisan serve --port=8004" `
  "cd chat-service && php artisan serve --port=8005" `
  "cd crs-frontend && npm run dev"