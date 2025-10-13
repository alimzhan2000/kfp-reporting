"""
API views для управления пользователями с базой данных
"""
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.contrib.auth.models import User
from .models import UserProfile
import json
import logging
import traceback

logger = logging.getLogger(__name__)

@csrf_exempt
@require_http_methods(["POST"])
def create_user(request):
    """Создание нового пользователя"""
    try:
        data = json.loads(request.body)
        
        # Проверка обязательных полей
        required_fields = ['username', 'password', 'role']
        for field in required_fields:
            if not data.get(field):
                return JsonResponse({
                    'success': False,
                    'error': f'Поле {field} обязательно для заполнения'
                }, status=400)
        
        # Валидация роли
        valid_roles = ['admin', 'manager', 'user']
        if data['role'] not in valid_roles:
            return JsonResponse({
                'success': False,
                'error': f'Недопустимая роль. Доступные роли: {", ".join(valid_roles)}'
            }, status=400)
        
        # Создание пользователя
        user = User.objects.create(
            username=data['username'],
            password=make_password(data['password']),
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            email=data.get('email', ''),
            is_active=True
        )
        
        # Создание профиля
        profile = UserProfile.objects.create(
            user=user,
            role=data['role'],
            phone=data.get('phone', ''),
            department=data.get('department', ''),
            is_active_user=data.get('is_active_user', True)
        )
        
        return JsonResponse({
            'success': True,
            'message': f'Пользователь {user.username} успешно создан',
            'user': {
                'id': user.id,
                'username': user.username,
                'role': profile.role,
                'role_display': profile.role_display,
                'full_name': profile.get_full_name(),
                'email': user.email,
                'phone': profile.phone,
                'department': profile.department,
                'is_active_user': profile.is_active_user,
                'is_active': user.is_active,
                'created_at': profile.created_at.isoformat()
            }
        })
        
    except IntegrityError as e:
        if 'username' in str(e):
            return JsonResponse({
                'success': False,
                'error': 'Пользователь с таким именем уже существует'
            }, status=400)
        return JsonResponse({
            'success': False,
            'error': 'Ошибка создания пользователя'
        }, status=400)
        
    except ValidationError as e:
        return JsonResponse({
            'success': False,
            'error': f'Ошибка валидации: {str(e)}'
        }, status=400)
        
    except Exception as e:
        logger.error(f'Error creating user: {str(e)}')
        return JsonResponse({
            'success': False,
            'error': 'Внутренняя ошибка сервера'
        }, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def list_users(request):
    """Получение списка всех пользователей"""
    try:
        users = User.objects.select_related('profile').all().order_by('-date_joined')
        
        users_data = []
        for user in users:
            profile = getattr(user, 'profile', None)
            users_data.append({
                'id': user.id,
                'username': user.username,
                'role': profile.role if profile else 'user',
                'role_display': profile.role_display if profile else 'Пользователь',
                'full_name': profile.get_full_name() if profile else f"{user.first_name} {user.last_name}".strip() or user.username,
                'email': user.email,
                'phone': profile.phone if profile else '',
                'department': profile.department if profile else '',
                'is_active_user': profile.is_active_user if profile else True,
                'is_active': user.is_active,
                'last_login': user.last_login.isoformat() if user.last_login else None,
                'created_at': profile.created_at.isoformat() if profile else user.date_joined.isoformat(),
                'updated_at': profile.updated_at.isoformat() if profile else user.date_joined.isoformat()
            })
        
        return JsonResponse({
            'success': True,
            'users': users_data,
            'total': len(users_data)
        })
        
    except Exception as e:
        logger.error(f'Error listing users: {str(e)}')
        return JsonResponse({
            'success': False,
            'error': 'Ошибка получения списка пользователей'
        }, status=500)

@csrf_exempt
@require_http_methods(["PUT"])
def update_user(request, user_id):
    """Обновление пользователя"""
    try:
        data = json.loads(request.body)
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Пользователь не найден'
            }, status=404)
        
        # Получаем или создаем профиль
        profile, created = UserProfile.objects.get_or_create(
            user=user,
            defaults={'role': 'user', 'is_active_user': True}
        )
        
        # Обновление полей пользователя
        if 'username' in data:
            user.username = data['username']
        if 'password' in data and data['password']:
            user.password = make_password(data['password'])
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'email' in data:
            user.email = data['email']
        if 'is_active' in data:
            user.is_active = data['is_active']
        
        # Обновление полей профиля
        if 'role' in data:
            valid_roles = ['admin', 'manager', 'user']
            if data['role'] not in valid_roles:
                return JsonResponse({
                    'success': False,
                    'error': f'Недопустимая роль. Доступные роли: {", ".join(valid_roles)}'
                }, status=400)
            profile.role = data['role']
        if 'phone' in data:
            profile.phone = data['phone']
        if 'department' in data:
            profile.department = data['department']
        if 'is_active_user' in data:
            profile.is_active_user = data['is_active_user']
        
        user.save()
        profile.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Пользователь {user.username} успешно обновлен',
            'user': {
                'id': user.id,
                'username': user.username,
                'role': profile.role,
                'role_display': profile.role_display,
                'full_name': profile.get_full_name(),
                'email': user.email,
                'phone': profile.phone,
                'department': profile.department,
                'is_active_user': profile.is_active_user,
                'is_active': user.is_active,
                'updated_at': profile.updated_at.isoformat()
            }
        })
        
    except IntegrityError as e:
        if 'username' in str(e):
            return JsonResponse({
                'success': False,
                'error': 'Пользователь с таким именем уже существует'
            }, status=400)
        return JsonResponse({
            'success': False,
            'error': 'Ошибка обновления пользователя'
        }, status=400)
        
    except Exception as e:
        logger.error(f'Error updating user: {str(e)}')
        return JsonResponse({
            'success': False,
            'error': 'Ошибка обновления пользователя'
        }, status=500)

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_user(request, user_id):
    """Удаление пользователя"""
    try:
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Пользователь не найден'
            }, status=404)
        
        username = user.username
        user.delete()  # Это также удалит связанный профиль из-за CASCADE
        
        return JsonResponse({
            'success': True,
            'message': f'Пользователь {username} успешно удален'
        })
        
    except Exception as e:
        logger.error(f'Error deleting user: {str(e)}')
        return JsonResponse({
            'success': False,
            'error': 'Ошибка удаления пользователя'
        }, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def get_user(request, user_id):
    """Получение информации о конкретном пользователе"""
    try:
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Пользователь не найден'
            }, status=404)
        
        profile = getattr(user, 'profile', None)
        
        return JsonResponse({
            'success': True,
            'user': {
                'id': user.id,
                'username': user.username,
                'role': profile.role if profile else 'user',
                'role_display': profile.role_display if profile else 'Пользователь',
                'full_name': profile.get_full_name() if profile else f"{user.first_name} {user.last_name}".strip() or user.username,
                'email': user.email,
                'phone': profile.phone if profile else '',
                'department': profile.department if profile else '',
                'is_active_user': profile.is_active_user if profile else True,
                'is_active': user.is_active,
                'last_login': user.last_login.isoformat() if user.last_login else None,
                'created_at': profile.created_at.isoformat() if profile else user.date_joined.isoformat(),
                'updated_at': profile.updated_at.isoformat() if profile else user.date_joined.isoformat()
            }
        })
        
    except Exception as e:
        logger.error(f'Error getting user: {str(e)}')
        return JsonResponse({
            'success': False,
            'error': 'Ошибка получения информации о пользователе'
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def initialize_demo_users(request):
    """Инициализация демо-пользователей в базе данных"""
    try:
        # Проверяем подключение к базе данных
        from django.db import connection
        connection.ensure_connection()
        
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
        errors = []
        
        for user_data in demo_users:
            try:
                # Проверяем, существует ли пользователь
                if User.objects.filter(username=user_data['username']).exists():
                    logger.info(f'User {user_data["username"]} already exists, skipping')
                    continue
                
                # Создаем пользователя
                user = User.objects.create(
                    username=user_data['username'],
                    password=make_password(user_data['password']),
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                    email=user_data['email'],
                    is_active=True
                )
                logger.info(f'Created user: {user.username}')
                
                # Создаем профиль
                profile = UserProfile.objects.create(
                    user=user,
                    role=user_data['role'],
                    phone=user_data['phone'],
                    department=user_data['department'],
                    is_active_user=user_data['is_active_user']
                )
                logger.info(f'Created profile for user: {user.username} with role: {profile.role}')
                
                created_count += 1
                
            except Exception as user_error:
                error_msg = f'Error creating user {user_data["username"]}: {str(user_error)}'
                logger.error(error_msg)
                errors.append(error_msg)
        
        if errors:
            return JsonResponse({
                'success': False,
                'error': f'Частичная ошибка. Создано: {created_count}, Ошибки: {"; ".join(errors)}',
                'created_count': created_count,
                'errors': errors
            }, status=500)
        
        return JsonResponse({
            'success': True,
            'message': f'Создано {created_count} демо-пользователей',
            'created_count': created_count
        })
        
    except Exception as e:
        error_msg = f'Критическая ошибка инициализации: {str(e)}'
        logger.error(error_msg)
        logger.error(f'Full traceback: {traceback.format_exc()}')
        return JsonResponse({
            'success': False,
            'error': error_msg
        }, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def check_database_status(request):
    """Проверка состояния базы данных"""
    try:
        from django.db import connection
        
        # Проверяем подключение к базе данных
        connection.ensure_connection()
        
        # Проверяем, существуют ли нужные таблицы
        auth_user_exists = False
        userprofile_exists = False
        
        try:
            # Пытаемся выполнить простой запрос к таблицам
            User.objects.count()
            auth_user_exists = True
        except:
            pass
            
        try:
            UserProfile.objects.count()
            userprofile_exists = True
        except:
            pass
        
        # Проверяем, есть ли пользователи
        user_count = User.objects.count()
        profile_count = UserProfile.objects.count()
        
        return JsonResponse({
            'success': True,
            'database_connection': True,
            'tables': {
                'auth_user': auth_user_exists,
                'accounts_userprofile': userprofile_exists
            },
            'counts': {
                'users': user_count,
                'profiles': profile_count
            },
            'message': 'База данных работает корректно'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'database_connection': False,
            'error': f'Ошибка подключения к базе данных: {str(e)}'
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def force_initialize_database(request):
    """Принудительная инициализация базы данных с применением миграций"""
    try:
        from django.core.management import call_command
        from django.db import connection
        
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
        errors = []
        
        for user_data in demo_users:
            try:
                # Удаляем существующего пользователя если есть
                if User.objects.filter(username=user_data['username']).exists():
                    User.objects.filter(username=user_data['username']).delete()
                
                # Создаем пользователя
                user = User.objects.create(
                    username=user_data['username'],
                    password=make_password(user_data['password']),
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                    email=user_data['email'],
                    is_active=True
                )
                logger.info(f'Created user: {user.username}')
                
                # Создаем профиль
                profile = UserProfile.objects.create(
                    user=user,
                    role=user_data['role'],
                    phone=user_data['phone'],
                    department=user_data['department'],
                    is_active_user=user_data['is_active_user']
                )
                logger.info(f'Created profile for user: {user.username} with role: {profile.role}')
                
                created_count += 1
                
            except Exception as user_error:
                error_msg = f'Error creating user {user_data["username"]}: {str(user_error)}'
                logger.error(error_msg)
                errors.append(error_msg)
        
        if errors:
            return JsonResponse({
                'success': False,
                'error': f'Частичная ошибка. Создано: {created_count}, Ошибки: {"; ".join(errors)}',
                'created_count': created_count,
                'errors': errors
            }, status=500)
        
        return JsonResponse({
            'success': True,
            'message': f'База данных инициализирована! Создано {created_count} демо-пользователей',
            'created_count': created_count
        })
        
    except Exception as e:
        error_msg = f'Критическая ошибка инициализации базы данных: {str(e)}'
        logger.error(error_msg)
        logger.error(f'Full traceback: {traceback.format_exc()}')
        return JsonResponse({
            'success': False,
            'error': error_msg
        }, status=500)