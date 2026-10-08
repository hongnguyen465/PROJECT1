# Free all microservices and frontend ports if held by old background processes
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

$env:PHP_CLI_SERVER_WORKERS = "8"

npx concurrently -n "GATEWAY,AUTH,CATALOG,ORDER,PAY,CHAT,FRONTEND" `
  -c "blue,magenta,yellow,cyan,blue,red,green" `
  "cd api-gateway && php artisan serve --port=8000" `
  "cd auth-service && php artisan serve --port=8001" `
  "cd catalog-service && php artisan serve --port=8002" `
  "cd order-service && php artisan serve --port=8003" `
  "cd payment-service && php artisan serve --port=8004" `
  "cd chat-service && php artisan serve --port=8005" `
  "cd crs-frontend && npm run dev"