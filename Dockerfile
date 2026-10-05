# Stage 1: Build Frontend React SPA
FROM node:20-alpine AS frontend-builder
WORKDIR /app
COPY crs-frontend/package*.json ./
RUN npm ci
COPY crs-frontend/ ./
RUN npm run build

# Stage 2: Final Production Image with PHP 8.4 & Nginx
FROM php:8.4-cli-alpine AS production
ENV COMPOSER_ALLOW_SUPERUSER=1

RUN apk add --no-cache bash nginx curl git unzip gettext tini ca-certificates \
    libpng libzip oniguruma \
    && apk add --no-cache --virtual .build-deps $PHPIZE_DEPS \
    libpng-dev libzip-dev oniguruma-dev \
    && docker-php-ext-install -j"$(nproc)" pdo_mysql mbstring zip gd bcmath opcache \
    && apk del .build-deps

COPY --from=composer:2 /usr/bin/composer /usr/local/bin/composer

WORKDIR /var/www

# Copy all backend source code
COPY api-gateway/ ./api-gateway/
COPY auth-service/ ./auth-service/
COPY catalog-service/ ./catalog-service/
COPY order-service/ ./order-service/
COPY payment-service/ ./payment-service/

# Install PHP dependencies without post-dump artisan scripts for all services
RUN cd api-gateway && composer install --prefer-dist --no-interaction --no-scripts --ignore-platform-reqs && cd .. \
    && cd auth-service && composer install --prefer-dist --no-interaction --no-scripts --ignore-platform-reqs && cd .. \
    && cd catalog-service && composer install --prefer-dist --no-interaction --no-scripts --ignore-platform-reqs && cd .. \
    && cd order-service && composer install --prefer-dist --no-interaction --no-scripts --ignore-platform-reqs && cd .. \
    && cd payment-service && composer install --prefer-dist --no-interaction --no-scripts --ignore-platform-reqs && cd ..

# Copy built frontend
COPY --from=frontend-builder /app/dist /var/www/crs-frontend/dist

# Copy Docker Nginx config & Entrypoint
COPY docker/nginx.conf /etc/nginx/templates/default.conf.template
COPY docker/php.ini /usr/local/etc/php/conf.d/zz-app.ini
COPY --chmod=755 docker/entrypoint.sh /usr/local/bin/app-entrypoint

RUN mkdir -p /run/nginx

ENV APP_ENV=production APP_DEBUG=false LOG_CHANNEL=stderr LOG_LEVEL=info \
    APP_KEY=base64:7B8M4oZq5q3k9u8r7t6w5e4r3t2y1u0i9o8p7a6s5d4= \
    JWT_SECRET=striker_super_secret_jwt_key_2026_production_123456789 \
    DB_CONNECTION=mysql SESSION_DRIVER=database SESSION_SECURE_COOKIE=true \
    CACHE_STORE=database QUEUE_CONNECTION=sync PORT=10000 RUN_MIGRATIONS=true RUN_SEEDERS=true

EXPOSE 10000

HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD curl --fail --silent "http://127.0.0.1:${PORT}/up" > /dev/null || exit 1

ENTRYPOINT ["/sbin/tini", "--", "/usr/local/bin/app-entrypoint"]
