#!/bin/bash

# 🚀 Скрипт для автоматической настройки Railway проекта
# Использование: ./railway-setup.sh

set -e

echo "🚀 Настройка Railway проекта для KFP Reporting..."

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Функция для вывода сообщений
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Проверка наличия Railway CLI
if ! command -v railway &> /dev/null; then
    log_info "Установка Railway CLI..."
    npm install -g @railway/cli
fi

# Проверка токена
if [ -z "$RAILWAY_TOKEN" ]; then
    log_error "RAILWAY_TOKEN не установлен!"
    log_info "Установите токен: export RAILWAY_TOKEN=ваш-токен"
    exit 1
fi

log_info "Настройка переменных окружения..."

# Основные переменные Django
railway variables set SECRET_KEY="django-insecure-$(openssl rand -base64 32)" --service kfp-reporting
railway variables set DEBUG=False --service kfp-reporting
railway variables set DJANGO_SETTINGS_MODULE=kfp_reporting.settings --service kfp-reporting
railway variables set ALLOWED_HOSTS="*" --service kfp-reporting

# CORS настройки (будут обновлены после получения домена)
railway variables set CORS_ALLOW_CREDENTIALS=True --service kfp-reporting
railway variables set CORS_ALLOW_ALL_ORIGINS=False --service kfp-reporting
railway variables set CORS_ALLOWED_HEADERS="accept,accept-encoding,authorization,content-type,dnt,origin,user-agent,x-csrftoken,x-requested-with" --service kfp-reporting
railway variables set CORS_EXPOSE_HEADERS="content-type,x-csrftoken" --service kfp-reporting
railway variables set CORS_PREFLIGHT_MAX_AGE=86400 --service kfp-reporting

# Cookie настройки для HTTPS
railway variables set SESSION_COOKIE_SECURE=True --service kfp-reporting
railway variables set CSRF_COOKIE_SECURE=True --service kfp-reporting
railway variables set SESSION_COOKIE_SAMESITE=None --service kfp-reporting
railway variables set CSRF_COOKIE_SAMESITE=None --service kfp-reporting
railway variables set SESSION_COOKIE_HTTPONLY=False --service kfp-reporting
railway variables set CSRF_COOKIE_HTTPONLY=False --service kfp-reporting

log_success "Переменные окружения настроены!"

# Получение домена
log_info "Получение домена приложения..."
DOMAIN=$(railway domain --service kfp-reporting 2>/dev/null || echo "")

if [ -z "$DOMAIN" ]; then
    log_warning "Домен не найден. Создайте домен в Railway Dashboard:"
    log_info "1. Откройте Railway Dashboard"
    log_info "2. Выберите ваш проект"
    log_info "3. Выберите сервис kfp-reporting"
    log_info "4. Перейдите в Settings → Domains"
    log_info "5. Нажмите 'Generate Domain'"
    log_info "6. Скопируйте полученный URL"
    echo ""
    read -p "Введите ваш домен (например: https://kfp-reporting-production.up.railway.app): " DOMAIN
fi

if [ ! -z "$DOMAIN" ]; then
    log_info "Обновление CORS настроек для домена: $DOMAIN"
    railway variables set CORS_ALLOWED_ORIGINS="$DOMAIN" --service kfp-reporting
    railway variables set CORS_TRUSTED_ORIGINS="$DOMAIN" --service kfp-reporting
    log_success "CORS настроен для домена: $DOMAIN"
fi

# Деплой
log_info "Запуск деплоя..."
railway up --service kfp-reporting --detach

log_success "Деплой запущен!"

# Ожидание завершения деплоя
log_info "Ожидание завершения деплоя..."
sleep 30

# Проверка статуса
log_info "Проверка статуса приложения..."
if [ ! -z "$DOMAIN" ]; then
    if curl -s -f "$DOMAIN/api/" > /dev/null; then
        log_success "Приложение успешно развернуто!"
        log_info "URL: $DOMAIN"
        log_info "API: $DOMAIN/api/"
        log_info "Admin: $DOMAIN/admin/"
    else
        log_warning "Приложение может быть еще не готово. Проверьте логи в Railway Dashboard."
    fi
else
    log_info "Проверьте статус в Railway Dashboard"
fi

echo ""
log_success "Настройка завершена!"
echo ""
log_info "Следующие шаги:"
echo "1. Выполните миграции: railway run python manage.py migrate"
echo "2. Создайте суперпользователя: railway run python manage.py createsuperuser"
echo "3. Проверьте логи в Railway Dashboard"
echo "4. Откройте приложение: $DOMAIN"
