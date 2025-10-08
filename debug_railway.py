#!/usr/bin/env python
"""
Скрипт для диагностики проблем Railway
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

def check_environment():
    """Проверка переменных окружения"""
    print("🔍 Проверка переменных окружения:")
    required_vars = ['SECRET_KEY', 'DEBUG', 'ALLOWED_HOSTS']
    
    for var in required_vars:
        value = os.environ.get(var, 'НЕ УСТАНОВЛЕНО')
        print(f"  {var}: {value}")
    
    # Проверка DATABASE_URL
    db_url = os.environ.get('DATABASE_URL', 'НЕ УСТАНОВЛЕНО')
    print(f"  DATABASE_URL: {'УСТАНОВЛЕНО' if db_url != 'НЕ УСТАНОВЛЕНО' else 'НЕ УСТАНОВЛЕНО'}")
    
    # Проверка Railway переменных
    railway_vars = ['RAILWAY_PUBLIC_DOMAIN', 'RAILWAY_STATIC_URL', 'PORT']
    for var in railway_vars:
        value = os.environ.get(var, 'НЕ УСТАНОВЛЕНО')
        print(f"  {var}: {value}")

def check_django_setup():
    """Проверка настройки Django"""
    print("\n🔍 Проверка настройки Django:")
    try:
        django.setup()
        print("  ✅ Django успешно настроен")
        
        # Проверка приложений
        from django.conf import settings
        print(f"  INSTALLED_APPS: {len(settings.INSTALLED_APPS)} приложений")
        print(f"  DEBUG: {settings.DEBUG}")
        print(f"  ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
        
        # Проверка базы данных
        db_config = settings.DATABASES['default']
        print(f"  DATABASE ENGINE: {db_config['ENGINE']}")
        
    except Exception as e:
        print(f"  ❌ Ошибка настройки Django: {e}")

def check_models():
    """Проверка моделей"""
    print("\n🔍 Проверка моделей:")
    try:
        from accounts.models import User
        from reports.models import AgriculturalData
        print("  ✅ Модели успешно импортированы")
        
        # Проверка миграций
        from django.core.management import execute_from_command_line
        print("  ✅ Django management команды доступны")
        
    except Exception as e:
        print(f"  ❌ Ошибка импорта моделей: {e}")

def check_dependencies():
    """Проверка зависимостей"""
    print("\n🔍 Проверка зависимостей:")
    required_packages = [
        'django', 'djangorestframework', 'django_cors_headers',
        'psycopg2', 'gunicorn', 'whitenoise', 'python_decouple'
    ]
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} - НЕ УСТАНОВЛЕН")

def main():
    print("🚀 Диагностика Railway проекта")
    print("=" * 50)
    
    check_environment()
    check_dependencies()
    check_django_setup()
    check_models()
    
    print("\n" + "=" * 50)
    print("✅ Диагностика завершена")

if __name__ == '__main__':
    main()
