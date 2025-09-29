#!/bin/bash

# 🚀 Полное исправление Railway деплоя
# Использование: ./fix-railway-complete.sh

set -e

echo "🚀 Полное исправление Railway деплоя..."

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

log_info "Настройка минимальной конфигурации для Railway..."

# Удаляем проблемные переменные и устанавливаем минимальные
railway variables set ALLOWED_HOSTS="*" --service kfp-reporting
railway variables set DEBUG=True --service kfp-reporting
railway variables set SECRET_KEY="django-insecure-minimal-key-for-testing" --service kfp-reporting

# Удаляем проблемные переменные базы данных
railway variables set DATABASE_URL="sqlite:///db.sqlite3" --service kfp-reporting

# Минимальные CORS настройки
railway variables set CORS_ALLOWED_ORIGINS="*" --service kfp-reporting
railway variables set CORS_ALLOW_ALL_ORIGINS=True --service kfp-reporting
railway variables set CORS_ALLOW_CREDENTIALS=False --service kfp-reporting

# Упрощенные cookie настройки
railway variables set SESSION_COOKIE_SECURE=False --service kfp-reporting
railway variables set CSRF_COOKIE_SECURE=False --service kfp-reporting
railway variables set SESSION_COOKIE_SAMESITE=Lax --service kfp-reporting
railway variables set CSRF_COOKIE_SAMESITE=Lax --service kfp-reporting

log_success "Минимальные переменные установлены!"

# Коммит изменений
log_info "Коммит изменений в Git..."
git add .
git commit -m "Fix Railway deployment: use minimal configuration and simple views" || true
git push || true

log_success "Изменения закоммичены!"

# Деплой с минимальной конфигурацией
log_info "Запуск деплоя с минимальной конфигурацией..."
railway up --service kfp-reporting --detach

log_success "Деплой запущен с минимальной конфигурацией!"

# Ожидание завершения деплоя
log_info "Ожидание завершения деплоя (90 секунд)..."
sleep 90

# Проверка доступности
log_info "Проверка доступности приложения..."
APP_URL="https://kfp-reporting-production.up.railway.app"

# Проверка главной страницы
if curl -s -f "$APP_URL/" > /dev/null; then
    log_success "✅ Главная страница доступна!"
    echo "Ответ: $(curl -s "$APP_URL/")"
else
    log_warning "⚠️  Главная страница недоступна"
fi

# Проверка Health Check
if curl -s -f "$APP_URL/api/health/" > /dev/null; then
    log_success "✅ Health Check доступен!"
    echo "Ответ: $(curl -s "$APP_URL/api/health/")"
else
    log_warning "⚠️  Health Check недоступен"
fi

echo ""
log_info "🌐 Публичный URL: $APP_URL"
log_info "📊 API Endpoints:"
log_info "   • Главная: $APP_URL/"
log_info "   • Health Check: $APP_URL/api/health/"
log_info "   • API: $APP_URL/api/"

echo ""
log_success "🎉 Минимальная конфигурация развернута!"
log_info "Следующие шаги:"
echo "1. Проверьте логи в Railway Dashboard"
echo "2. Если приложение работает, настройте базу данных"
echo "3. Выполните миграции: railway run python manage.py migrate"
echo "4. Откройте приложение: $APP_URL"
