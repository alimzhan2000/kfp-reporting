#!/usr/bin/env python
"""
Скрипт для исправления views.py - заменяет функцию home на оригинальный дизайн
"""

def fix_views_file():
    """Исправляет файл views.py"""
    
    # Читаем текущий файл
    with open('/Users/alimzhankenesbekov/kfp-reporting/kfp_reporting/views.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Находим начало и конец функции home
    start_marker = '@csrf_exempt\ndef home(request):'
    end_marker = '@csrf_exempt\ndef upload_page(request):'
    
    start_pos = content.find(start_marker)
    end_pos = content.find(end_marker)
    
    if start_pos == -1 or end_pos == -1:
        print("Не удалось найти маркеры для замены")
        return False
    
    # Создаем новую функцию home
    new_home_function = '''@csrf_exempt
def home(request):
    """
    Главная страница - показывает KFP Reporting dashboard с оригинальным дизайном
    """
    return HttpResponse(get_original_dashboard(), content_type="text/html")

'''
    
    # Заменяем функцию
    new_content = content[:start_pos] + new_home_function + content[end_pos:]
    
    # Записываем исправленный файл
    with open('/Users/alimzhankenesbekov/kfp-reporting/kfp_reporting/views.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("Файл views.py успешно исправлен!")
    return True

if __name__ == '__main__':
    fix_views_file()
