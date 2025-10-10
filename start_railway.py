#!/usr/bin/env python
"""
Скрипт запуска для Railway
Читает переменную PORT из окружения и запускает Django
"""
import os
import sys
import subprocess

def main():
    # Получаем порт из переменной окружения
    port = os.environ.get('PORT', '8000')
    
    print(f"Starting Django on port: {port}")
    print(f"Environment PORT: {os.environ.get('PORT', 'NOT SET')}")
    
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
