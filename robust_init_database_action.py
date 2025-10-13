from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
@require_http_methods(["POST"])
def robust_init_database_action(request):
    """
    Надежная инициализация базы данных с созданием таблиц через SQL
    """
    try:
        from django.db import connection
        from django.contrib.auth.models import User
        from accounts.models import UserProfile
        from django.contrib.auth.hashers import make_password
        from django.utils import timezone
        
        logger.info('Starting robust database initialization...')
        
        # Проверяем подключение к базе данных
        connection.ensure_connection()
        
        # Создаем таблицы напрямую через SQL, если они не существуют
        with connection.cursor() as cursor:
            # Создаем таблицу auth_user, если она не существует
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS auth_user (
                    id SERIAL PRIMARY KEY,
                    password VARCHAR(128) NOT NULL,
                    last_login TIMESTAMP WITH TIME ZONE,
                    is_superuser BOOLEAN NOT NULL,
                    username VARCHAR(150) NOT NULL UNIQUE,
                    first_name VARCHAR(150) NOT NULL,
                    last_name VARCHAR(150) NOT NULL,
                    email VARCHAR(254) NOT NULL,
                    is_staff BOOLEAN NOT NULL,
                    is_active BOOLEAN NOT NULL,
                    date_joined TIMESTAMP WITH TIME ZONE NOT NULL
                )
            """)
            
            # Создаем таблицу accounts_userprofile, если она не существует
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS accounts_userprofile (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
                    role VARCHAR(50) NOT NULL,
                    phone VARCHAR(20),
                    department VARCHAR(100),
                    is_active_user BOOLEAN NOT NULL DEFAULT TRUE,
                    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
                    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
                )
            """)
            
            # Создаем таблицу reports_agriculturaldata, если она не существует
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reports_agriculturaldata (
                    id SERIAL PRIMARY KEY,
                    field_name VARCHAR(200) NOT NULL,
                    year INTEGER NOT NULL,
                    variety VARCHAR(200) NOT NULL,
                    final_product VARCHAR(200) NOT NULL,
                    planting_area DECIMAL(10,2) NOT NULL,
                    yield_per_hectare DECIMAL(10,2) NOT NULL,
                    total_yield DECIMAL(10,2) NOT NULL,
                    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
                    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
                )
            """)
            
            # Создаем таблицу reports_reporttemplate, если она не существует
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reports_reporttemplate (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(200) NOT NULL,
                    description TEXT,
                    template_type VARCHAR(50) NOT NULL,
                    is_active BOOLEAN NOT NULL DEFAULT TRUE,
                    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
                    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
                )
            """)
            
            # Создаем дополнительные таблицы Django Auth, если они не существуют
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS auth_user_groups (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
                    group_id INTEGER NOT NULL,
                    UNIQUE(user_id, group_id)
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS auth_user_user_permissions (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
                    permission_id INTEGER NOT NULL,
                    UNIQUE(user_id, permission_id)
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS auth_group (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(150) NOT NULL UNIQUE
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS auth_permission (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    content_type_id INTEGER NOT NULL,
                    codename VARCHAR(100) NOT NULL,
                    UNIQUE(content_type_id, codename)
                )
            """)
            
            logger.info('Database tables created successfully')
        
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
        logger.error(f'Robust database initialization error: {str(e)}')
        return JsonResponse({
            'success': False,
            'error': f'Ошибка инициализации базы данных: {str(e)}'
        })
