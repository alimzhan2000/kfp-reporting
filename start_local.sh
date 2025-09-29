#!/bin/bash

# Скрипт для локального запуска проекта Reporting KFP (без Docker)

echo "🚀 Запуск Reporting KFP локально..."

# Проверяем наличие Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 не установлен. Пожалуйста, установите Python 3 и повторите попытку."
    exit 1
fi

# Проверяем наличие Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js не установлен. Установите Node.js с https://nodejs.org/"
    exit 1
fi

# Проверяем наличие PostgreSQL
if ! command -v psql &> /dev/null; then
    echo "❌ PostgreSQL не установлен. Установите PostgreSQL:"
    echo "   brew install postgresql"
    echo "   brew services start postgresql"
    exit 1
fi

echo "✅ Все необходимые компоненты найдены"

# Создаем виртуальное окружение Python
echo "🐍 Создание виртуального окружения Python..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Активируем виртуальное окружение
source venv/bin/activate

# Устанавливаем зависимости Python
echo "📦 Установка зависимостей Python..."
pip install -r requirements.txt

# Создаем .env файл если его нет
if [ ! -f .env ]; then
    echo "📝 Создание файла .env..."
    cp env.example .env
    echo "✅ Файл .env создан. При необходимости отредактируйте его."
fi

# Создаем базу данных PostgreSQL
echo "🗄️  Настройка базы данных..."
createdb kfp_reporting 2>/dev/null || echo "База данных уже существует"

# Применяем миграции
echo "📊 Применение миграций..."
python manage.py migrate

# Собираем статические файлы
echo "📁 Сборка статических файлов..."
python manage.py collectstatic --noinput

# Инициализируем базу данных
echo "👤 Инициализация базы данных..."
python init_db.py

# Устанавливаем зависимости Node.js
echo "📦 Установка зависимостей Node.js..."
cd frontend
npm install
cd ..

echo ""
echo "🎉 Проект настроен!"
echo ""
echo "📋 Для запуска выполните следующие команды:"
echo ""
echo "1. Запустите backend (в одном терминале):"
echo "   source venv/bin/activate"
echo "   python manage.py runserver"
echo ""
echo "2. Запустите frontend (в другом терминале):"
echo "   cd frontend"
echo "   npm start"
echo ""
echo "📱 После запуска доступны URL:"
echo "   Frontend:  http://localhost:3000"
echo "   Backend:   http://localhost:8000"
echo "   Admin:     http://localhost:8000/admin/"
echo ""
echo "👤 Данные для входа:"
echo "   Администратор: admin/admin123"
echo "   Руководство:  management/management123"
echo ""

