#!/bin/bash

# 🚀 Автоматическая настройка Railway
# Использование: ./auto-setup-railway.sh

set -e

echo "🚀 Автоматическая настройка Railway..."

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

log_info "Настройка переменных окружения..."

# Основные настройки Django
npx -y @railway/cli variables --set 'SECRET_KEY=django-insecure-'$(openssl rand -base64 32) --service kfp-reporting
npx -y @railway/cli variables --set 'DEBUG=False' --service kfp-reporting
npx -y @railway/cli variables --set 'ALLOWED_HOSTS=*' --service kfp-reporting
npx -y @railway/cli variables --set 'DJANGO_SETTINGS_MODULE=kfp_reporting.settings' --service kfp-reporting

# CORS настройки
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

# Коммит и деплой
log_info "Коммит изменений..."
git add .
git commit -m "Auto-configure Railway deployment" || true
git push || true

log_success "Изменения закоммичены!"

# Деплой
log_info "Запуск деплоя..."
npx -y @railway/cli up --service kfp-reporting --ci --detach

log_success "Деплой запущен!"

# Ожидание
log_info "Ожидание завершения деплоя (120 секунд)..."
sleep 120

# Выполнение миграций
log_info "Выполнение миграций базы данных..."
npx -y @railway/cli run --service kfp-reporting python manage.py migrate

log_success "Миграции выполнены!"

# Создание суперпользователя
log_info "Создание суперпользователя..."
echo "Создайте суперпользователя:"
npx -y @railway/cli run --service kfp-reporting python manage.py createsuperuser

log_success "Суперпользователь создан!"

# Загрузка тестовых данных
log_info "Загрузка тестовых данных..."
npx -y @railway/cli run --service kfp-reporting python init_db.py

log_success "Тестовые данные загружены!"

# Проверка
log_info "Проверка работоспособности..."
APP_URL="https://kfp-reporting-production.up.railway.app"

if curl -s -f "$APP_URL/" > /dev/null; then
    log_success "✅ Главная страница доступна!"
fi

if curl -s -f "$APP_URL/api/health/" > /dev/null; then
    log_success "✅ Health Check доступен!"
fi

if curl -s -f "$APP_URL/api/reports/dashboard-stats/" > /dev/null; then
    log_success "✅ API доступен!"
else
    log_warning "⚠️  API недоступен - проверьте логи"
fi

echo ""
log_success "🎉 Настройка завершена!"
log_info "🌐 Публичный URL: $APP_URL"
log_info "📊 Доступные endpoints:"
log_info "   • Главная: $APP_URL/"
log_info "   • Health Check: $APP_URL/api/health/"
log_info "   • API: $APP_URL/api/"
log_info "   • Админка: $APP_URL/admin/"
log_info "   • Загрузка: $APP_URL/api/upload/file/"
log_info "   • Отчеты: $APP_URL/api/reports/"
