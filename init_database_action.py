from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
@require_http_methods(["POST"])
def init_database_action(request):
    """
    Простая инициализация базы данных
    """
    try:
        from django.core.management import call_command
        from django.db import connection
        from django.contrib.auth.models import User
        from accounts.models import UserProfile
        from django.contrib.auth.hashers import make_password
        from django.utils import timezone
        
        logger.info('Starting database initialization...')
        
        # Применяем миграции
        try:
            call_command('migrate', verbosity=0)
            logger.info('Migrations applied successfully')
        except Exception as e:
            logger.error(f'Error applying migrations: {str(e)}')
            return JsonResponse({
                'success': False,
                'error': f'Ошибка применения миграций: {str(e)}'
            })
        
        # Проверяем подключение к базе данных
        connection.ensure_connection()
        
        # Создаем демо-пользователей
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
                'department': 'Управление',
                'is_active_user': True
            }
        ]
        
        created_users = []
        
        for user_data in demo_users:
            try:
                # Проверяем, существует ли пользователь
                if User.objects.filter(username=user_data['username']).exists():
                    logger.info(f'User {user_data["username"]} already exists')
                    continue
                
                # Создаем пользователя
                user = User.objects.create_user(
                    username=user_data['username'],
                    password=user_data['password'],
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                    email=user_data['email'],
                    is_staff=True,
                    is_superuser=(user_data['role'] == 'admin')
                )
                
                # Создаем профиль пользователя
                UserProfile.objects.create(
                    user=user,
                    role=user_data['role'],
                    phone=user_data['phone'],
                    department=user_data['department'],
                    is_active_user=user_data['is_active_user']
                )
                
                created_users.append(user_data['username'])
                logger.info(f'Created user: {user_data["username"]}')
                
            except Exception as e:
                logger.error(f'Error creating user {user_data["username"]}: {str(e)}')
                return JsonResponse({
                    'success': False,
                    'error': f'Ошибка создания пользователя {user_data["username"]}: {str(e)}'
                })
        
        return JsonResponse({
            'success': True,
            'message': f'База данных успешно инициализирована! Создано пользователей: {len(created_users)}',
            'users': created_users
        })
        
    except Exception as e:
        logger.error(f'Database initialization error: {str(e)}')
        return JsonResponse({
            'success': False,
            'error': f'Ошибка инициализации базы данных: {str(e)}'
        })
