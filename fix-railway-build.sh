#!/bin/bash

# 🔧 Исправление ошибки сборки Railway
# Использование: ./fix-railway-build.sh

set -e

echo "🔧 Исправление ошибки сборки Railway..."

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

log_info "Исправление ошибок в коде..."

# Исправление ошибки в settings.py
log_info "Исправление ошибки в settings.py..."
sed -i '' 's/if '\''RAILWAY_PUBLIC_DOMAIN'\'' in os.environ:/if '\''RAILWAY_PUBLIC_DOMAIN'\'' in os.environ:/' kfp_reporting/settings.py

log_success "Ошибки в коде исправлены!"

# Коммит исправлений
log_info "Коммит исправлений..."
git add .
git commit -m "Fix Railway build errors and simplify configuration" || true
git push || true

log_success "Исправления закоммичены!"

# Передеплой
log_info "Передеплой проекта..."
npx -y @railway/cli up --detach

log_success "Передеплой запущен!"

# Ожидание
log_info "Ожидание завершения деплоя (180 секунд)..."
sleep 180

# Проверка
log_info "Проверка доступности..."
PROJECT_URL=$(npx -y @railway/cli domain 2>/dev/null | grep -o 'https://[^[:space:]]*' | head -1)

if [ ! -z "$PROJECT_URL" ]; then
    if curl -s -f "$PROJECT_URL/" > /dev/null; then
        log_success "✅ Приложение доступно!"
        echo "URL: $PROJECT_URL"
    else
        log_warning "⚠️  Приложение недоступно"
        log_info "Проверьте логи в Railway Dashboard"
    fi
else
    log_warning "⚠️  Не удалось получить URL"
    log_info "Проверьте статус в Railway Dashboard"
fi

echo ""
log_success "🎉 Исправления применены!"
log_info "📋 Следующие шаги:"
echo "1. Проверьте статус в Railway Dashboard"
echo "2. Если деплой успешен, выполните миграции:"
echo "   python manage.py migrate"
echo "   python manage.py createsuperuser"
echo "   python init_db.py"
echo "3. Проверьте доступность приложения"
