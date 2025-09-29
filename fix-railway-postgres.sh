#!/bin/bash

# 🔧 Исправление Railway с PostgreSQL
# Использование: ./fix-railway-postgres.sh

set -e

echo "🔧 Исправление Railway с PostgreSQL..."

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

log_info "Настройка переменных окружения для PostgreSQL..."

# Основные настройки Django
npx -y @railway/cli variables --set 'DEBUG=False' --service kfp-reporting
npx -y @railway/cli variables --set 'ALLOWED_HOSTS=*' --service kfp-reporting
npx -y @railway/cli variables --set 'DJANGO_SETTINGS_MODULE=kfp_reporting.settings' --service kfp-reporting

# CORS настройки для публичного доступа
npx -y @railway/cli variables --set 'CORS_ALLOWED_ORIGINS=https://kfp-reporting-production.up.railway.app' --service kfp-reporting
npx -y @railway/cli variables --set 'CORS_TRUSTED_ORIGINS=https://kfp-reporting-production.up.railway.app' --service kfp-reporting
npx -y @railway/cli variables --set 'CORS_ALLOW_CREDENTIALS=True' --service kfp-reporting
npx -y @railway/cli variables --set 'CORS_ALLOW_ALL_ORIGINS=False' --service kfp-reporting

# Cookie настройки для HTTPS
npx -y @railway/cli variables --set 'SESSION_COOKIE_SECURE=True' --service kfp-reporting
npx -y @railway/cli variables --set 'CSRF_COOKIE_SECURE=True' --service kfp-reporting
npx -y @railway/cli variables --set 'SESSION_COOKIE_SAMESITE=None' --service kfp-reporting
npx -y @railway/cli variables --set 'CSRF_COOKIE_SAMESITE=None' --service kfp-reporting
npx -y @railway/cli variables --set 'SESSION_COOKIE_HTTPONLY=False' --service kfp-reporting
npx -y @railway/cli variables --set 'CSRF_COOKIE_HTTPONLY=False' --service kfp-reporting

log_success "Переменные окружения настроены!"

# Коммит изменений
log_info "Коммит изменений в Git..."
git add .
git commit -m "Fix Railway PostgreSQL configuration with Gunicorn" || true
git push || true

log_success "Изменения закоммичены!"

# Деплой с исправлениями
log_info "Запуск деплоя с исправлениями..."
npx -y @railway/cli up --service kfp-reporting --ci --detach

log_success "Деплой запущен!"

# Ожидание завершения деплоя
log_info "Ожидание завершения деплоя (120 секунд)..."
sleep 120

# Проверка доступности
log_info "Проверка доступности приложения..."
APP_URL="https://kfp-reporting-production.up.railway.app"

# Проверка главной страницы
if curl -s -f "$APP_URL/" > /dev/null; then
    log_success "✅ Главная страница доступна!"
    echo "Ответ: $(curl -s "$APP_URL/" | head -3)"
else
    log_warning "⚠️  Главная страница недоступна"
fi

# Проверка Health Check
if curl -s -f "$APP_URL/api/health/" > /dev/null; then
    log_success "✅ Health Check доступен!"
    echo "Ответ: $(curl -s "$APP_URL/api/health/" | head -3)"
else
    log_warning "⚠️  Health Check недоступен"
fi

# Проверка API
if curl -s -f "$APP_URL/api/reports/dashboard-stats/" > /dev/null; then
    log_success "✅ API доступен!"
    echo "Ответ: $(curl -s "$APP_URL/api/reports/dashboard-stats/" | head -3)"
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
echo "2. Создайте суперпользователя: railway run python manage.py createsuperuser"
echo "3. Загрузите тестовые данные: railway run python init_db.py"
echo "4. Откройте приложение: $APP_URL"
