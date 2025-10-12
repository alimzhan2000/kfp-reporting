#!/usr/bin/env python
"""
Скрипт для исправления yield_comparison_report в views.py
"""

def fix_yield_report():
    """Исправляет функцию yield_comparison_report в views.py"""
    
    # Читаем текущий файл
    with open('/Users/alimzhankenesbekov/kfp-reporting/kfp_reporting/views.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Находим начало и конец функции yield_comparison_report
    start_marker = '@csrf_exempt\ndef yield_comparison_report(request):'
    end_marker = '@csrf_exempt\ndef test_upload_page(request):'
    
    start_pos = content.find(start_marker)
    end_pos = content.find(end_marker)
    
    if start_pos == -1 or end_pos == -1:
        print("Не удалось найти маркеры для замены")
        return False
    
    # Создаем новую функцию yield_comparison_report
    new_yield_function = '''@csrf_exempt
def yield_comparison_report(request):
    """Отчет сравнения урожайности с оригинальным дизайном"""
    return HttpResponse(get_original_yield_comparison_report(), content_type="text/html")

'''
    
    # Заменяем функцию
    new_content = content[:start_pos] + new_yield_function + content[end_pos:]
    
    # Записываем исправленный файл
    with open('/Users/alimzhankenesbekov/kfp-reporting/kfp_reporting/views.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("Функция yield_comparison_report успешно исправлена!")
    return True

if __name__ == '__main__':
    fix_yield_report()
