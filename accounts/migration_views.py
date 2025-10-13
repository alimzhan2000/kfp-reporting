"""
Дополнительные views для работы с миграциями
"""
import json
import logging
import traceback
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

logger = logging.getLogger(__name__)

@csrf_exempt
@require_http_methods(["GET"])
def check_migrations_status(request):
    """Проверка статуса миграций"""
    try:
        from django.core.management import call_command
        from django.db import connection
        from io import StringIO
        import sys
        
        # Проверяем подключение к базе данных
        connection.ensure_connection()
        
        # Получаем список примененных миграций
        output = StringIO()
        old_stdout = sys.stdout
        sys.stdout = output
        
        try:
            call_command('showmigrations', verbosity=0)
            migrations_output = output.getvalue()
        finally:
            sys.stdout = old_stdout
        
        # Проверяем, есть ли непримененные миграции
        unapplied_migrations = []
        for line in migrations_output.split('\n'):
            if line.strip() and '[ ]' in line:
                unapplied_migrations.append(line.strip())
        
        return JsonResponse({
            'success': True,
            'database_connection': True,
            'unapplied_migrations': unapplied_migrations,
            'total_unapplied': len(unapplied_migrations),
            'message': f'Найдено {len(unapplied_migrations)} непримененных миграций'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'database_connection': False,
            'error': f'Ошибка проверки миграций: {str(e)}'
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def apply_migrations(request):
    """Применение миграций"""
    try:
        from django.core.management import call_command
        from django.db import connection
        
        # Проверяем подключение к базе данных
        connection.ensure_connection()
        
        # Применяем миграции
        try:
            call_command('migrate', verbosity=0)
            logger.info('Migrations applied successfully')
        except Exception as e:
            logger.error(f'Error applying migrations: {str(e)}')
            return JsonResponse({
                'success': False,
                'error': f'Ошибка применения миграций: {str(e)}'
            }, status=500)
        
        return JsonResponse({
            'success': True,
            'message': 'Миграции применены успешно'
        })
        
    except Exception as e:
        error_msg = f'Критическая ошибка применения миграций: {str(e)}'
        logger.error(error_msg)
        logger.error(f'Full traceback: {traceback.format_exc()}')
        return JsonResponse({
            'success': False,
            'error': error_msg
        }, status=500)
