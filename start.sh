#!/bin/bash

# Скрипт для запуска проекта Reporting KFP

echo "🚀 Запуск Reporting KFP..."

# Проверяем наличие Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен. Пожалуйста, установите Docker и повторите попытку."
    exit 1
fi

# Проверяем наличие Docker Compose
if ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose не установлен. Пожалуйста, установите Docker Compose и повторите попытку."
    exit 1
fi

# Создаем .env файл если его нет
if [ ! -f .env ]; then
    echo "📝 Создание файла .env..."
    cp env.example .env
    echo "✅ Файл .env создан. При необходимости отредактируйте его."
fi

# Останавливаем существующие контейнеры
echo "🛑 Остановка существующих контейнеров..."
docker compose down

# Собираем и запускаем контейнеры
echo "🔨 Сборка и запуск контейнеров..."
docker compose up --build -d

# Ждем запуска базы данных
echo "⏳ Ожидание запуска базы данных..."
sleep 10

# Применяем миграции
echo "📊 Применение миграций..."
docker compose exec -T backend python manage.py migrate

# Собираем статические файлы
echo "📁 Сборка статических файлов..."
docker compose exec -T backend python manage.py collectstatic --noinput

# Инициализируем базу данных
echo "👤 Инициализация базы данных..."
docker compose exec -T backend python init_db.py

echo ""
echo "🎉 Reporting KFP успешно запущен!"
echo ""
echo "📱 Доступные URL:"
echo "   Frontend:  http://localhost:3000"
echo "   Backend:   http://localhost:8000"
echo "   Admin:     http://localhost:8000/admin/"
echo ""
echo "👤 Данные для входа:"
echo "   Администратор: admin/admin123"
echo "   Руководство:  management/management123"
echo ""
echo "📋 Полезные команды:"
echo "   Остановить:  docker compose down"
echo "   Логи:        docker compose logs -f"
echo "   Перезапуск:  docker compose restart"
echo ""
echo "🔧 Для разработки:"
echo "   Backend shell:  docker compose exec backend python manage.py shell"
echo "   Создать миграцию: docker compose exec backend python manage.py makemigrations"
echo ""
