#!/bin/bash

# 🌐 Скрипт для настройки публичного доступа Railway
# Использование: ./setup-public-access.sh

set -e

echo "🌐 Настройка публичного доступа для KFP Reporting..."

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

log_info "Обновление переменных окружения для публичного доступа..."

# Обновление CORS настроек для публичного доступа
railway variables set CORS_ALLOWED_ORIGINS="https://kfp-reporting-production.up.railway.app" --service kfp-reporting
railway variables set CORS_TRUSTED_ORIGINS="https://kfp-reporting-production.up.railway.app" --service kfp-reporting

log_success "CORS настройки обновлены!"

# Деплой с обновленными настройками
log_info "Запуск деплоя с обновленными настройками..."
railway up --service kfp-reporting --detach

log_success "Деплой запущен!"

# Ожидание завершения деплоя
log_info "Ожидание завершения деплоя..."
sleep 30

# Проверка доступности
log_info "Проверка доступности приложения..."
APP_URL="https://kfp-reporting-production.up.railway.app"

if curl -s -f "$APP_URL/api/" > /dev/null; then
    log_success "Приложение успешно развернуто и доступно!"
    echo ""
    log_info "🌐 Публичный URL: $APP_URL"
    log_info "📊 API Endpoints:"
    log_info "   • Главная: $APP_URL/api/"
    log_info "   • Админка: $APP_URL/admin/"
    log_info "   • Загрузка: $APP_URL/api/upload/file/"
    log_info "   • Отчеты: $APP_URL/api/reports/"
    log_info "   • Статистика: $APP_URL/api/reports/dashboard-stats/"
    echo ""
    log_success "🎉 Приложение готово к использованию!"
else
    log_warning "Приложение может быть еще не готово. Проверьте логи в Railway Dashboard."
    log_info "URL: $APP_URL"
fi

echo ""
log_info "Следующие шаги:"
echo "1. Выполните миграции: railway run python manage.py migrate"
echo "2. Создайте суперпользователя: railway run python manage.py createsuperuser"
echo "3. Проверьте логи в Railway Dashboard"
echo "4. Откройте приложение: $APP_URL"
