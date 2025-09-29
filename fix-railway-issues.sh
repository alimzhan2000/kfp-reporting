#!/bin/bash

# 🔧 Исправление проблем Railway
# Использование: ./fix-railway-issues.sh

set -e

echo "🔧 Исправление проблем Railway..."

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

APP_URL="https://kfp-reporting-production.up.railway.app"

log_info "Проверка текущего состояния..."

# Проверка главной страницы
if curl -s -f "$APP_URL/" > /dev/null; then
    log_success "✅ Главная страница доступна"
else
    log_error "❌ Главная страница недоступна"
fi

# Проверка Health Check
if curl -s -f "$APP_URL/api/health/" > /dev/null; then
    log_success "✅ Health Check доступен"
else
    log_error "❌ Health Check недоступен"
fi

# Проверка API
if curl -s -f "$APP_URL/api/reports/dashboard-stats/" > /dev/null; then
    log_success "✅ API доступен"
else
    log_warning "⚠️  API недоступен - выполняем исправления..."
    
    log_info "Выполнение миграций..."
    npx -y @railway/cli run --service kfp-reporting python manage.py migrate
    
    log_info "Создание суперпользователя..."
    npx -y @railway/cli run --service kfp-reporting python manage.py createsuperuser
    
    log_info "Загрузка тестовых данных..."
    npx -y @railway/cli run --service kfp-reporting python init_db.py
    
    log_success "Исправления выполнены!"
fi

# Финальная проверка
log_info "Финальная проверка..."
sleep 30

if curl -s -f "$APP_URL/api/reports/dashboard-stats/" > /dev/null; then
    log_success "✅ API теперь доступен!"
    echo "Ответ: $(curl -s "$APP_URL/api/reports/dashboard-stats/" | head -3)"
else
    log_warning "⚠️  API все еще недоступен"
    log_info "Проверьте логи в Railway Dashboard"
fi

echo ""
log_success "🎉 Проверка завершена!"
log_info "🌐 Публичный URL: $APP_URL"
