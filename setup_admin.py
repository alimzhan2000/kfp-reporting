#!/usr/bin/env python
"""
Скрипт для настройки админа через Railway
"""
import os
import django
from django.core.management import execute_from_command_line

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kfp_reporting.settings')
django.setup()

def setup_admin():
    """Создает суперпользователя если его нет"""
    from django.contrib.auth import get_user_model
    
    User = get_user_model()
    
    # Проверяем, есть ли уже суперпользователь
    if User.objects.filter(is_superuser=True).exists():
        print("Суперпользователь уже существует!")
        return
    
    # Данные для суперпользователя
    username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
    email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@kfp-reporting.com')
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')
    
    # Создаем суперпользователя
    user = User.objects.create_superuser(username, email, password)
    print(f"✅ Суперпользователь создан:")
    print(f"Username: {username}")
    print(f"Email: {email}")
    print(f"Password: {password}")
    print(f"\n🌐 Теперь вы можете войти в admin панель:")
    print(f"https://kfp-reporting.up.railway.app/admin/")

if __name__ == '__main__':
    setup_admin()
