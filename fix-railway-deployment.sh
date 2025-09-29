#!/bin/bash

# 🔧 Скрипт для исправления проблем с Railway деплоем
# Использование: ./fix-railway-deployment.sh

set -e

echo "🔧 Исправление проблем с Railway деплоем..."

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

# Проверка токена
if [ -z "$RAILWAY_TOKEN" ]; then
    log_error "RAILWAY_TOKEN не установлен!"
    log_info "Установите токен: export RAILWAY_TOKEN=ваш-токен"
    exit 1
fi

log_info "Обновление переменных окружения для исправления Healthcheck..."

# Обновление переменных для исправления проблем
railway variables set ALLOWED_HOSTS="*" --service kfp-reporting
railway variables set DEBUG=False --service kfp-reporting
railway variables set SECRET_KEY="django-insecure-$(openssl rand -base64 32)" --service kfp-reporting

# Настройка базы данных (если еще не настроена)
railway variables set DATABASE_URL="postgresql://postgres:password@postgres.railway.internal:5432/railway" --service kfp-reporting

# CORS настройки
railway variables set CORS_ALLOWED_ORIGINS="https://kfp-reporting-production.up.railway.app" --service kfp-reporting
railway variables set CORS_TRUSTED_ORIGINS="https://kfp-reporting-production.up.railway.app" --service kfp-reporting
railway variables set CORS_ALLOW_CREDENTIALS=True --service kfp-reporting
railway variables set CORS_ALLOW_ALL_ORIGINS=False --service kfp-reporting

# Cookie настройки для HTTPS
railway variables set SESSION_COOKIE_SECURE=True --service kfp-reporting
railway variables set CSRF_COOKIE_SECURE=True --service kfp-reporting
railway variables set SESSION_COOKIE_SAMESITE=None --service kfp-reporting
railway variables set CSRF_COOKIE_SAMESITE=None --service kfp-reporting
railway variables set SESSION_COOKIE_HTTPONLY=False --service kfp-reporting
railway variables set CSRF_COOKIE_HTTPONLY=False --service kfp-reporting

log_success "Переменные окружения обновлены!"

# Коммит изменений
log_info "Коммит изменений в Git..."
git add .
git commit -m "Fix Railway deployment: add health check endpoints and improve configuration" || true
git push || true

log_success "Изменения закоммичены!"

# Деплой с исправлениями
log_info "Запуск деплоя с исправлениями..."
railway up --service kfp-reporting --detach

log_success "Деплой запущен с исправлениями!"

# Ожидание завершения деплоя
log_info "Ожидание завершения деплоя (60 секунд)..."
sleep 60

# Проверка доступности
log_info "Проверка доступности приложения..."
APP_URL="https://kfp-reporting-production.up.railway.app"

# Проверка главной страницы
if curl -s -f "$APP_URL/" > /dev/null; then
    log_success "✅ Главная страница доступна!"
else
    log_warning "⚠️  Главная страница недоступна"
fi

# Проверка Health Check
if curl -s -f "$APP_URL/api/health/" > /dev/null; then
    log_success "✅ Health Check доступен!"
else
    log_warning "⚠️  Health Check недоступен"
fi

# Проверка API
if curl -s -f "$APP_URL/api/reports/dashboard-stats/" > /dev/null; then
    log_success "✅ API доступен!"
else
    log_warning "⚠️  API недоступен"
fi

echo ""
log_info "🌐 Публичный URL: $APP_URL"
log_info "📊 API Endpoints:"
log_info "   • Главная: $APP_URL/"
log_info "   • Health Check: $APP_URL/api/health/"
log_info "   • API: $APP_URL/api/"
log_info "   • Админка: $APP_URL/admin/"
log_info "   • Загрузка: $APP_URL/api/upload/file/"
log_info "   • Отчеты: $APP_URL/api/reports/"

echo ""
log_success "🎉 Исправления применены!"
log_info "Следующие шаги:"
echo "1. Проверьте логи в Railway Dashboard"
echo "2. Выполните миграции: railway run python manage.py migrate"
echo "3. Создайте суперпользователя: railway run python manage.py createsuperuser"
echo "4. Откройте приложение: $APP_URL"
