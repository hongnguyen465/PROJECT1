# Stage 1: Build Frontend React SPA
FROM node:20-alpine AS frontend-builder
WORKDIR /app
COPY crs-frontend/package*.json ./
RUN npm ci
COPY crs-frontend/ ./
RUN npm run build

# Stage 2: Base PHP environment with all required tools (git, unzip, curl, nginx, extensions)
FROM php:8.3-cli-alpine AS php-base
ENV COMPOSER_ALLOW_SUPERUSER=1

RUN apk add --no-cache bash nginx curl git unzip gettext tini ca-certificates \
    libpng libzip oniguruma \
    && apk add --no-cache --virtual .build-deps $PHPIZE_DEPS \
    libpng-dev libzip-dev oniguruma-dev \
    && docker-php-ext-install -j"$(nproc)" pdo_mysql mbstring zip gd bcmath opcache \
    && apk del .build-deps

COPY --from=composer:2 /usr/bin/composer /usr/local/bin/composer

# Stage 3: Install PHP dependencies for all services
FROM php-base AS backend-builder
WORKDIR /var/www

COPY api-gateway/composer.json api-gateway/composer.lock ./api-gateway/
COPY auth-service/composer.json auth-service/composer.lock ./auth-service/
COPY catalog-service/composer.json catalog-service/composer.lock ./catalog-service/
COPY order-service/composer.json order-service/composer.lock ./order-service/
COPY payment-service/composer.json payment-service/composer.lock ./payment-service/

RUN cd api-gateway && composer install --no-dev --prefer-dist --no-interaction --no-scripts --no-autoloader --ignore-platform-reqs && cd .. \
    && cd auth-service && composer install --no-dev --prefer-dist --no-interaction --no-scripts --no-autoloader --ignore-platform-reqs && cd .. \
    && cd catalog-service && composer install --no-dev --prefer-dist --no-interaction --no-scripts --no-autoloader --ignore-platform-reqs && cd .. \
    && cd order-service && composer install --no-dev --prefer-dist --no-interaction --no-scripts --no-autoloader --ignore-platform-reqs && cd .. \
    && cd payment-service && composer install --no-dev --prefer-dist --no-interaction --no-scripts --no-autoloader --ignore-platform-reqs && cd ..

COPY api-gateway/ ./api-gateway/
COPY auth-service/ ./auth-service/
COPY catalog-service/ ./catalog-service/
COPY order-service/ ./order-service/
COPY payment-service/ ./payment-service/

RUN cd api-gateway && composer dump-autoload --no-dev --optimize && cd .. \
    && cd auth-service && composer dump-autoload --no-dev --optimize && cd .. \
    && cd catalog-service && composer dump-autoload --no-dev --optimize && cd .. \
    && cd order-service && composer dump-autoload --no-dev --optimize && cd .. \
    && cd payment-service && composer dump-autoload --no-dev --optimize && cd ..

# Stage 4: Final Production Image
FROM php-base AS production

ENV APP_ENV=production APP_DEBUG=false LOG_CHANNEL=stderr LOG_LEVEL=info \
    DB_CONNECTION=mysql SESSION_DRIVER=database SESSION_SECURE_COOKIE=true \
    CACHE_STORE=database QUEUE_CONNECTION=sync PORT=10000 RUN_MIGRATIONS=true RUN_SEEDERS=true

WORKDIR /var/www

# Copy built frontend
COPY --from=frontend-builder /app/dist /var/www/crs-frontend/dist

# Copy backend microservices
COPY --from=backend-builder /var/www /var/www

# Copy Docker Nginx config & Entrypoint
COPY docker/nginx.conf /etc/nginx/templates/default.conf.template
COPY docker/php.ini /usr/local/etc/php/conf.d/zz-app.ini
COPY --chmod=755 docker/entrypoint.sh /usr/local/bin/app-entrypoint

RUN mkdir -p /run/nginx

EXPOSE 10000

HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD curl --fail --silent "http://127.0.0.1:${PORT}/up" > /dev/null || exit 1

ENTRYPOINT ["/sbin/tini", "--", "/usr/local/bin/app-entrypoint"]
