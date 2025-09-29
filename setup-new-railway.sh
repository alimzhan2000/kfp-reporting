#!/bin/bash

# 🆕 Настройка нового проекта Railway
# Использование: ./setup-new-railway.sh

set -e

echo "🆕 Настройка нового проекта Railway..."

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

log_info "Создание нового проекта Railway..."

# Создание нового проекта
log_info "Создание проекта из GitHub репозитория..."
npx -y @railway/cli init --template github:alimzhan2000/kfp-reporting

log_success "Проект создан!"

# Добавление PostgreSQL
log_info "Добавление PostgreSQL базы данных..."
npx -y @railway/cli add postgres

log_success "PostgreSQL добавлен!"

# Настройка переменных окружения
log_info "Настройка переменных окружения..."

# Основные настройки Django
npx -y @railway/cli variables --set 'SECRET_KEY=django-insecure-'$(openssl rand -base64 32)
npx -y @railway/cli variables --set 'DEBUG=False'
npx -y @railway/cli variables --set 'ALLOWED_HOSTS=*'
npx -y @railway/cli variables --set 'DJANGO_SETTINGS_MODULE=kfp_reporting.settings'

# CORS настройки (будут обновлены после получения домена)
npx -y @railway/cli variables --set 'CORS_ALLOWED_ORIGINS=https://placeholder.up.railway.app'
npx -y @railway/cli variables --set 'CORS_TRUSTED_ORIGINS=https://placeholder.up.railway.app'
npx -y @railway/cli variables --set 'CORS_ALLOW_CREDENTIALS=True'
npx -y @railway/cli variables --set 'CORS_ALLOW_ALL_ORIGINS=False'

# Cookie настройки для HTTPS
npx -y @railway/cli variables --set 'SESSION_COOKIE_SECURE=True'
npx -y @railway/cli variables --set 'CSRF_COOKIE_SECURE=True'
npx -y @railway/cli variables --set 'SESSION_COOKIE_SAMESITE=None'
npx -y @railway/cli variables --set 'CSRF_COOKIE_SAMESITE=None'
npx -y @railway/cli variables --set 'SESSION_COOKIE_HTTPONLY=False'
npx -y @railway/cli variables --set 'CSRF_COOKIE_HTTPONLY=False'

log_success "Переменные окружения настроены!"

# Деплой
log_info "Запуск деплоя..."
npx -y @railway/cli up --detach

log_success "Деплой запущен!"

# Ожидание завершения деплоя
log_info "Ожидание завершения деплоя (180 секунд)..."
sleep 180

# Получение публичного URL
log_info "Получение публичного URL..."
PUBLIC_URL=$(npx -y @railway/cli domain 2>/dev/null | grep -o 'https://[^[:space:]]*' | head -1)

if [ -z "$PUBLIC_URL" ]; then
    log_warning "Не удалось получить публичный URL автоматически"
    log_info "Пожалуйста, получите URL вручную из Railway Dashboard"
    log_info "Затем обновите CORS настройки:"
    echo "npx -y @railway/cli variables --set 'CORS_ALLOWED_ORIGINS=https://ваш-домен.up.railway.app'"
    echo "npx -y @railway/cli variables --set 'CORS_TRUSTED_ORIGINS=https://ваш-домен.up.railway.app'"
else
    log_success "Публичный URL: $PUBLIC_URL"
    
    # Обновление CORS настройки с реальным URL
    log_info "Обновление CORS настройки с реальным URL..."
    npx -y @railway/cli variables --set "CORS_ALLOWED_ORIGINS=$PUBLIC_URL"
    npx -y @railway/cli variables --set "CORS_TRUSTED_ORIGINS=$PUBLIC_URL"
    
    log_success "CORS настройки обновлены!"
fi

# Проверка доступности
log_info "Проверка доступности приложения..."

if [ ! -z "$PUBLIC_URL" ]; then
    if curl -s -f "$PUBLIC_URL/" > /dev/null; then
        log_success "✅ Главная страница доступна!"
        echo "Ответ: $(curl -s "$PUBLIC_URL/" | head -3)"
    else
        log_warning "⚠️  Главная страница недоступна"
    fi

    if curl -s -f "$PUBLIC_URL/api/health/" > /dev/null; then
        log_success "✅ Health Check доступен!"
        echo "Ответ: $(curl -s "$PUBLIC_URL/api/health/" | head -3)"
    else
        log_warning "⚠️  Health Check недоступен"
    fi
fi

echo ""
log_success "🎉 Настройка нового проекта завершена!"
log_info "📋 Следующие шаги:"
echo "1. Откройте Railway Dashboard: https://railway.app/dashboard"
echo "2. Найдите ваш новый проект"
echo "3. Включите Public Networking в Settings → Networking"
echo "4. Выполните миграции в Terminal:"
echo "   python manage.py migrate"
echo "   python manage.py createsuperuser"
echo "   python init_db.py"
echo "5. Проверьте результат: $PUBLIC_URL"

if [ ! -z "$PUBLIC_URL" ]; then
    log_info "🌐 Публичный URL: $PUBLIC_URL"
    log_info "📊 Доступные endpoints:"
    log_info "   • Главная: $PUBLIC_URL/"
    log_info "   • Health Check: $PUBLIC_URL/api/health/"
    log_info "   • API: $PUBLIC_URL/api/"
    log_info "   • Админка: $PUBLIC_URL/admin/"
fi
