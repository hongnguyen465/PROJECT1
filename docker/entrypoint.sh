#!/bin/bash
set -Eeuo pipefail

# Render secret mounts may be readable by root but not by www-data.
# Copy only the CA certificate at runtime to an app-readable private location.
if [[ -n "${MYSQL_ATTR_SSL_CA:-}" ]]; then
    if [[ -f "$MYSQL_ATTR_SSL_CA" && -r "$MYSQL_ATTR_SSL_CA" ]]; then
        mkdir -p /run/app-certificates
        chmod 750 /run/app-certificates
        cp "$MYSQL_ATTR_SSL_CA" /run/app-certificates/mysql-ca.pem
        chmod 400 /run/app-certificates/mysql-ca.pem
        export MYSQL_ATTR_SSL_CA=/run/app-certificates/mysql-ca.pem
    fi
fi

# Allow maintenance commands with: docker run ... IMAGE ...
if (( $# > 0 )); then
    exec "$@"
fi

export PORT="${PORT:-10000}"

# Substitute PORT into Nginx template
envsubst '${PORT}' < /etc/nginx/templates/default.conf.template > /etc/nginx/http.d/default.conf

# Setup storage permissions for all microservices
for svc in api-gateway auth-service catalog-service order-service payment-service; do
    mkdir -p "/var/www/$svc/storage/framework/cache/data" \
             "/var/www/$svc/storage/framework/sessions" \
             "/var/www/$svc/storage/framework/views" \
             "/var/www/$svc/storage/logs" \
             "/var/www/$svc/storage/app/public" \
             "/var/www/$svc/bootstrap/cache"
    chmod -R 777 "/var/www/$svc/storage" "/var/www/$svc/bootstrap/cache"
done

# Run Migrations & Seeders if enabled
if [[ "${RUN_MIGRATIONS:-true}" == "true" ]]; then
    echo "=== Running database migrations ==="
    echo "1. Auth Service Migrations:"
    (cd /var/www/auth-service && php artisan migrate --force --no-interaction) || echo "Auth migration finished with notice"
    echo "2. Catalog Service Migrations:"
    (cd /var/www/catalog-service && php artisan migrate --force --no-interaction) || echo "Catalog migration finished with notice"
    echo "3. Order Service Migrations:"
    (cd /var/www/order-service && php artisan migrate --force --no-interaction) || echo "Order migration finished with notice"
    echo "4. Payment Service Migrations:"
    (cd /var/www/payment-service && php artisan migrate --force --no-interaction) || echo "Payment migration finished with notice"
fi

if [[ "${RUN_SEEDERS:-false}" == "true" ]]; then
    echo "=== Running database seeders ==="
    echo "1. Auth Service Seeders:"
    (cd /var/www/auth-service && php artisan db:seed --force --no-interaction) || echo "Auth seeder finished with notice"
    echo "2. Catalog Service Seeders:"
    (cd /var/www/catalog-service && php artisan db:seed --force --no-interaction) || echo "Catalog seeder finished with notice"
    echo "3. Order Service Seeders:"
    (cd /var/www/order-service && php artisan db:seed --force --no-interaction) || echo "Order seeder finished with notice"
fi

# Start all microservices in background
echo "Starting microservices..."
(cd /var/www/auth-service && php -S 0.0.0.0:8001 -t public &)
(cd /var/www/catalog-service && php -S 0.0.0.0:8002 -t public &)
(cd /var/www/order-service && php -S 0.0.0.0:8003 -t public &)
(cd /var/www/payment-service && php -S 0.0.0.0:8004 -t public &)
(cd /var/www/api-gateway && php -S 0.0.0.0:8000 -t public &)

# Start Nginx
echo "Starting Nginx reverse proxy on port $PORT..."
nginx -t
exec nginx -g 'daemon off;'
