#!/usr/bin/env python
"""
Скрипт для принудительного применения миграций на Railway
"""
import os
import sys
import subprocess

def main():
    print("🔄 Force applying migrations on Railway...")
    
    try:
        # Применяем все миграции
        print("📦 Applying all migrations...")
        result = subprocess.run([
            sys.executable, 'manage.py', 'migrate', '--run-syncdb'
        ], check=True, capture_output=True, text=True)
        
        print("✅ All migrations applied successfully!")
        print(result.stdout)
        
        # Проверяем статус миграций
        print("\n📋 Checking migration status...")
        status_result = subprocess.run([
            sys.executable, 'manage.py', 'showmigrations'
        ], check=True, capture_output=True, text=True)
        
        print(status_result.stdout)
        
        # Создаем суперпользователя
        print("\n👤 Creating superuser...")
        try:
            subprocess.run([
                sys.executable, 'manage.py', 'createsuperuser',
                '--username', 'admin',
                '--email', 'admin@kfp-reporting.com',
                '--noinput'
            ], check=True, input='admin123\nadmin123\n', text=True)
            print("✅ Superuser created!")
        except subprocess.CalledProcessError:
            print("⚠️ Superuser might already exist")
        
        print("\n🎉 Setup completed successfully!")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        print(f"Error output: {e.stderr}")
        sys.exit(1)

if __name__ == '__main__':
    main()
