Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "  CAI DAT DEPENDENCIES CHO TOAN BO MICROSERVICES" -ForegroundColor Yellow
Write-Host "========================================================" -ForegroundColor Cyan

$services = @("api-gateway", "auth-service", "catalog-service", "order-service", "payment-service", "chat-service")

foreach ($svc in $services) {
    Write-Host "`n[+] Dang cai dat Composer cho $svc..." -ForegroundColor Green
    if (Test-Path $svc) {
        Push-Location $svc
        composer install --no-interaction
        Pop-Location
    }
}

Write-Host "`n[+] Dang cai dat NPM packages cho crs-frontend..." -ForegroundColor Green
if (Test-Path "crs-frontend") {
    Push-Location "crs-frontend"
    npm install
    Pop-Location
}

Write-Host "`n========================================================" -ForegroundColor Cyan
Write-Host "  HOAN TAT! Ban co the chay .\start-all.bat de khoi dong!" -ForegroundColor Yellow
Write-Host "========================================================" -ForegroundColor Cyan
