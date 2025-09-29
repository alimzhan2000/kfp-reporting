#!/usr/bin/env python
"""
Скрипт для инициализации базы данных и создания тестовых данных
"""
import os
import sys
import django

# Добавляем путь к проекту
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Настраиваем Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kfp_reporting.settings')
django.setup()

from django.contrib.auth import get_user_model
from reports.models import AgriculturalData
import pandas as pd

User = get_user_model()

def create_superuser():
    """Создает суперпользователя если его нет"""
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123',
            first_name='Администратор',
            last_name='Системы',
            role='admin'
        )
        print("✅ Суперпользователь создан: admin/admin123")
    else:
        print("ℹ️  Суперпользователь уже существует")

def create_management_user():
    """Создает пользователя руководства"""
    if not User.objects.filter(username='management').exists():
        User.objects.create_user(
            username='management',
            email='management@example.com',
            password='management123',
            first_name='Руководство',
            last_name='Компании',
            role='management',
            phone='+7 (XXX) XXX-XX-XX',
            department='Руководство'
        )
        print("✅ Пользователь руководства создан: management/management123")
    else:
        print("ℹ️  Пользователь руководства уже существует")

def load_sample_data():
    """Загружает тестовые данные из CSV файла"""
    if AgriculturalData.objects.exists():
        print("ℹ️  Тестовые данные уже загружены")
        return
    
    try:
        # Получаем пользователя для загрузки
        user = User.objects.filter(role='admin').first()
        if not user:
            user = User.objects.first()
        
        # Читаем CSV файл
        df = pd.read_csv('sample_data.csv')
        
        # Создаем записи
        created_count = 0
        for _, row in df.iterrows():
            AgriculturalData.objects.create(
                field_name=row['Поле'],
                year=int(row['Год']),
                planting_area=float(row['Площадь посева']),
                yield_per_hectare=float(row['Урожайность ц/га']),
                crop=row['Культура'],
                variety=row['Сорт'],
                final_product=row['Конечный продукт'],
                uploaded_by=user
            )
            created_count += 1
        
        print(f"✅ Загружено {created_count} тестовых записей")
        
    except FileNotFoundError:
        print("⚠️  Файл sample_data.csv не найден, пропускаем загрузку тестовых данных")
    except Exception as e:
        print(f"❌ Ошибка загрузки тестовых данных: {e}")

def main():
    """Основная функция"""
    print("🚀 Инициализация базы данных...")
    
    # Создаем пользователей
    create_superuser()
    create_management_user()
    
    # Загружаем тестовые данные
    load_sample_data()
    
    print("\n🎉 Инициализация завершена!")
    print("\n📋 Доступные пользователи:")
    print("   Администратор: admin/admin123")
    print("   Руководство:  management/management123")

if __name__ == '__main__':
    main()

