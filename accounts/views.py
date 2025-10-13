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
                user = User.objects.create(
                    username=user_data['username'],
                    password=make_password(user_data['password']),
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                    email=user_data['email'],
                    is_active=True
                )
                
                UserProfile.objects.create(
                    user=user,
                    role=user_data['role'],
                    phone=user_data['phone'],
                    department=user_data['department'],
                    is_active_user=user_data['is_active_user']
                )
                created_count += 1
        
        return JsonResponse({
            'success': True,
            'message': f'Создано {created_count} демо-пользователей',
            'created_count': created_count
        })
        
    except Exception as e:
        logger.error(f'Error initializing demo users: {str(e)}')
        return JsonResponse({
            'success': False,
            'error': 'Ошибка инициализации демо-пользователей'
        }, status=500)