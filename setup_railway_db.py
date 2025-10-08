#!/usr/bin/env python
"""
Скрипт для автоматической настройки базы данных на Railway
"""
import os
import sys
import django
from pathlib import Path

# Добавляем путь к проекту
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kfp_reporting.settings')

def setup_database():
    """Настройка базы данных"""
    print("🚀 Настройка базы данных Railway")
    print("=" * 50)
    
    try:
        django.setup()
        from django.core.management import execute_from_command_line
        from django.db import connection
        
        # Проверяем подключение
        print("🔍 Проверка подключения к базе данных...")
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print("  ✅ Подключение к PostgreSQL успешно")
        
        # Выполняем миграции
        print("\n📋 Выполнение миграций...")
        execute_from_command_line(['manage.py', 'migrate'])
        print("  ✅ Миграции выполнены успешно")
        
        # Проверяем таблицы
        print("\n🔍 Проверка созданных таблиц...")
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """)
            tables = cursor.fetchall()
            print(f"  📋 Создано таблиц: {len(tables)}")
            for table in tables:
                print(f"    - {table[0]}")
        
        # Создаем суперпользователя
        print("\n👤 Создание суперпользователя...")
        print("  Введите данные для суперпользователя:")
        
        username = input("  Username (admin): ").strip() or "admin"
        email = input("  Email: ").strip()
        password = input("  Password: ").strip()
        
        if not password:
            print("  ❌ Пароль не может быть пустым")
            return False
        
        # Создаем суперпользователя
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        if User.objects.filter(username=username).exists():
            print(f"  ⚠️  Пользователь {username} уже существует")
        else:
            User.objects.create_superuser(username, email, password)
            print(f"  ✅ Суперпользователь {username} создан успешно")
        
        # Загружаем тестовые данные
        print("\n📊 Загрузка тестовых данных...")
        try:
            execute_from_command_line(['manage.py', 'shell', '-c', 'exec(open("init_db.py").read())'])
            print("  ✅ Тестовые данные загружены")
        except Exception as e:
            print(f"  ⚠️  Не удалось загрузить тестовые данные: {e}")
        
        print("\n🎉 Настройка базы данных завершена!")
        print("\n📋 Доступные endpoints:")
        print("  - Главная: https://ваш-домен.up.railway.app/")
        print("  - Админка: https://ваш-домен.up.railway.app/admin/")
        print("  - API: https://ваш-домен.up.railway.app/api/reports/")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка настройки базы данных: {e}")
        return False

if __name__ == '__main__':
    setup_database()
