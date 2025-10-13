#!/usr/bin/env python
"""
Скрипт для инициализации базы данных
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

def init_database():
    """Инициализация базы данных"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kfp_reporting.settings')
    django.setup()
    
    from django.core.management import call_command
    from django.contrib.auth.models import User
    from accounts.models import UserProfile
    from django.contrib.auth.hashers import make_password
    import datetime
    
    print("🔧 Инициализация базы данных...")
    
    # Применяем все миграции
    print("📦 Применение миграций...")
    try:
        call_command('migrate', verbosity=0)
        print("✅ Миграции применены успешно")
    except Exception as e:
        print(f"❌ Ошибка применения миграций: {e}")
        return False
    
    # Создаем демо-пользователей
    print("👥 Создание демо-пользователей...")
    demo_users = [
        {
            'username': 'admin',
            'password': 'admin123',
            'role': 'admin',
            'first_name': 'Администратор',
            'last_name': 'Системы',
            'email': 'admin@kfp.com',
            'phone': '+7 (777) 123-45-67',
            'department': 'IT',
            'is_active_user': True
        },
        {
            'username': 'manager',
            'password': 'manager123',
            'role': 'manager',
            'first_name': 'Менеджер',
            'last_name': 'Отдела',
            'email': 'manager@kfp.com',
            'phone': '+7 (777) 234-56-78',
            'department': 'Агрономия',
            'is_active_user': True
        },
        {
            'username': 'user',
            'password': 'user123',
            'role': 'user',
            'first_name': 'Пользователь',
            'last_name': 'Обычный',
            'email': 'user@kfp.com',
            'phone': '+7 (777) 345-67-89',
            'department': 'Поле',
            'is_active_user': True
        }
    ]
    
    created_count = 0
    for user_data in demo_users:
        if not User.objects.filter(username=user_data['username']).exists():
            try:
                user = User.objects.create(
                    username=user_data['username'],
                    password=make_password(user_data['password']),
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                    email=user_data['email'],
                    is_active=True,
                    date_joined=datetime.datetime.now()
                )
                
                UserProfile.objects.create(
                    user=user,
                    role=user_data['role'],
                    phone=user_data['phone'],
                    department=user_data['department'],
                    is_active_user=user_data['is_active_user'],
                    created_at=datetime.datetime.now(),
                    updated_at=datetime.datetime.now()
                )
                created_count += 1
                print(f"✅ Создан пользователь: {user_data['username']}")
            except Exception as e:
                print(f"❌ Ошибка создания пользователя {user_data['username']}: {e}")
        else:
            print(f"ℹ️  Пользователь {user_data['username']} уже существует")
    
    print(f"🎉 Инициализация завершена! Создано пользователей: {created_count}")
    return True

if __name__ == '__main__':
    success = init_database()
    sys.exit(0 if success else 1)
