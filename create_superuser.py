#!/usr/bin/env python
"""
Скрипт для создания суперпользователя Django
"""
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kfp_reporting.settings')
django.setup()

from django.contrib.auth import get_user_model

def create_superuser():
    User = get_user_model()
    
    # Проверяем, есть ли уже суперпользователь
    if User.objects.filter(is_superuser=True).exists():
        print("Суперпользователь уже существует!")
        return
    
    # Создаем суперпользователя
    username = 'admin'
    email = 'admin@kfp-reporting.com'
    password = 'admin123'  # Измените на более безопасный пароль
    
    user = User.objects.create_superuser(username, email, password)
    print(f"Суперпользователь создан:")
    print(f"Username: {username}")
    print(f"Email: {email}")
    print(f"Password: {password}")
    print(f"\nТеперь вы можете войти в admin панель по адресу:")
    print(f"https://kfp-reporting.up.railway.app/admin/")

if __name__ == '__main__':
    create_superuser()
