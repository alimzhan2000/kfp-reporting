#!/usr/bin/env python
"""
Скрипт запуска для Railway
Читает переменную PORT из окружения и запускает Django
"""
import os
import sys
import subprocess
from pathlib import Path

def setup_admin():
    """Создает суперпользователя если его нет"""
    try:
        print("🔧 Checking for admin user...")
        
        # Импортируем Django
        import django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kfp_reporting.settings')
        django.setup()
        
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        # Проверяем, есть ли уже суперпользователь
        if User.objects.filter(is_superuser=True).exists():
            print("✅ Admin user already exists!")
            return
        
        # Создаем суперпользователя
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@kfp-reporting.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')
        
        user = User.objects.create_superuser(username, email, password)
        print(f"✅ Admin user created:")
        print(f"   Username: {username}")
        print(f"   Email: {email}")
        print(f"   Password: {password}")
        print(f"🌐 Admin panel: https://kfp-reporting.up.railway.app/admin/")
        
    except Exception as e:
        print(f"⚠️  Could not create admin user: {e}")

def run_migrations():
    """Применяет миграции базы данных"""
    try:
        print("🔄 Running database migrations...")
        cmd = [sys.executable, 'manage.py', 'migrate']
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Migrations completed successfully!")
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Migration failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def main():
    # Получаем порт из переменной окружения
    port = os.environ.get('PORT', '8000')
    
    print(f"🚀 Starting Django on port: {port}")
    print(f"Environment PORT: {os.environ.get('PORT', 'NOT SET')}")
    
    # Применяем миграции перед запуском
    if not run_migrations():
        print("⚠️ Migrations failed, but continuing...")
    
    # Создаем админа перед запуском
    setup_admin()
    
    # Запускаем Django runserver
    cmd = [
        sys.executable, 'manage.py', 'runserver', 
        f'0.0.0.0:{port}', '--noreload'
    ]
    
    print(f"Running command: {' '.join(cmd)}")
    
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running Django: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
