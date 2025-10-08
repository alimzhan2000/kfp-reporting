#!/usr/bin/env python
"""
Скрипт для проверки подключения к базе данных
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

def check_database():
    """Проверка подключения к базе данных"""
    print("🔍 Проверка подключения к базе данных...")
    
    try:
        django.setup()
        from django.db import connection
        from django.core.management import execute_from_command_line
        
        # Проверяем подключение
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            print(f"  ✅ Подключение к базе данных успешно: {result}")
        
        # Проверяем таблицы
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """)
            tables = cursor.fetchall()
            print(f"  📋 Найдено таблиц: {len(tables)}")
            for table in tables:
                print(f"    - {table[0]}")
        
        # Проверяем миграции
        print("\n🔍 Проверка миграций...")
        execute_from_command_line(['manage.py', 'showmigrations'])
        
    except Exception as e:
        print(f"  ❌ Ошибка подключения к базе данных: {e}")
        return False
    
    return True

def main():
    print("🚀 Проверка базы данных Railway")
    print("=" * 50)
    
    if check_database():
        print("\n✅ База данных настроена корректно!")
    else:
        print("\n❌ Проблемы с базой данных. Выполните миграции:")
        print("   python manage.py migrate")

if __name__ == '__main__':
    main()
