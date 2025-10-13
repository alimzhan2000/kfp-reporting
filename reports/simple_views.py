"""
Простые views для тестирования API без аутентификации
"""
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from .models import AgriculturalData
from django.db.models import Avg, Sum


@csrf_exempt
@require_http_methods(["GET"])
def simple_dashboard_stats(request):
    """
    Простая статистика для дашборда без аутентификации
    """
    try:
        total_records = AgriculturalData.objects.count()
        unique_fields = AgriculturalData.objects.values('field_name').distinct().count()
        unique_products = AgriculturalData.objects.values('final_product').distinct().count()
        unique_varieties = AgriculturalData.objects.values('variety').distinct().count()
        
        # Последние данные
        latest_year = AgriculturalData.objects.values_list('year', flat=True).order_by('-year').first()
        
        # Средняя урожайность
        avg_yield = AgriculturalData.objects.aggregate(avg_yield=Avg('yield_per_hectare'))['avg_yield'] or 0
        
        # Общая площадь
        total_area = AgriculturalData.objects.aggregate(total_area=Sum('planting_area'))['total_area'] or 0
        
        return JsonResponse({
            'total_records': total_records,
            'unique_fields': unique_fields,
            'unique_products': unique_products,
            'unique_varieties': unique_varieties,
            'latest_year': latest_year,
            'avg_yield': round(avg_yield, 2),
            'total_area': round(total_area, 2)
        })
        
    except Exception as e:
        return JsonResponse({
            'error': f'Ошибка получения статистики: {str(e)}'
        }, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def simple_test_view(request):
    """
    Простой тест без аутентификации
    """
    return JsonResponse({
        'message': 'Простой API работает!',
        'status': 'success',
        'timestamp': timezone.now().isoformat()
    })


@csrf_exempt
@require_http_methods(["GET"])
def simple_yield_comparison(request):
    """
    Простое сравнение урожайности без аутентификации
    """
    try:
        from .services import ReportService
        
        filters = {
            'field_name': request.GET.get('field_name'),
            'year_from': request.GET.get('year_from'),
            'year_to': request.GET.get('year_to'),
            'final_product': request.GET.get('final_product'),
            'variety': request.GET.get('variety'),
        }
        
        # Убираем None значения
        filters = {k: v for k, v in filters.items() if v is not None}
        
        data = ReportService.get_yield_comparison_data(filters)
        return JsonResponse(data)
        
    except Exception as e:
        return JsonResponse({
            'error': f'Ошибка генерации отчета: {str(e)}'
        }, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def simple_field_efficiency(request):
    """
    Простая эффективность полей без аутентификации
    """
    try:
        from .services import ReportService
        
        filters = {
            'field_name': request.GET.get('field_name'),
            'year_from': request.GET.get('year_from'),
            'year_to': request.GET.get('year_to'),
            'final_product': request.GET.get('final_product'),
        }
        
        # Убираем None значения
        filters = {k: v for k, v in filters.items() if v is not None}
        
        data = ReportService.get_field_efficiency_data(filters)
        return JsonResponse(data)
        
    except Exception as e:
        return JsonResponse({
            'error': f'Ошибка генерации отчета: {str(e)}'
        }, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def simple_variety_performance(request):
    """
    Простая производительность сортов без аутентификации
    """
    try:
        from .services import ReportService
        
        filters = {
            'field_name': request.GET.get('field_name'),
            'year_from': request.GET.get('year_from'),
            'year_to': request.GET.get('year_to'),
            'final_product': request.GET.get('final_product'),
            'variety': request.GET.get('variety'),
        }
        
        # Убираем None значения
        filters = {k: v for k, v in filters.items() if v is not None}
        
        data = ReportService.get_variety_performance_data(filters)
        return JsonResponse(data)
        
    except Exception as e:
        return JsonResponse({
            'error': f'Ошибка генерации отчета: {str(e)}'
        }, status=500)


# Простые API endpoints для управления пользователями
@csrf_exempt
@require_http_methods(["GET"])
def simple_users_list(request):
    """
    Простой список пользователей без аутентификации
    """
    try:
        from django.contrib.auth.models import User
        from accounts.models import UserProfile
        
        users = []
        for user in User.objects.all():
            try:
                # Используем get_or_create для получения или создания профиля
                profile, created = UserProfile.objects.get_or_create(
                    user=user,
                    defaults={
                        'role': 'user',
                        'phone': '',
                        'department': '',
                        'is_active_user': True
                    }
                )
                users.append({
                    'id': user.id,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'is_active': user.is_active,
                    'date_joined': user.date_joined.isoformat(),
                    'role': profile.role,
                    'phone': profile.phone or '',
                    'department': profile.department or '',
                    'is_active_user': profile.is_active_user,
                    'created_at': profile.created_at.isoformat() if hasattr(profile, 'created_at') and profile.created_at else None,
                    'updated_at': profile.updated_at.isoformat() if hasattr(profile, 'updated_at') and profile.updated_at else None,
                })
            except Exception as e:
                # Если что-то пошло не так, создаем базовую запись пользователя
                users.append({
                    'id': user.id,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'is_active': user.is_active,
                    'date_joined': user.date_joined.isoformat(),
                    'role': 'user',
                    'phone': '',
                    'department': '',
                    'is_active_user': True,
                    'created_at': None,
                    'updated_at': None,
                })
        
        return JsonResponse({
            'success': True,
            'users': users,
            'count': len(users)
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Ошибка получения списка пользователей: {str(e)}'
        }, status=500)


@csrf_exempt
@require_http_methods(["DELETE"])
def simple_delete_user(request, user_id):
    """
    Удаление пользователя без аутентификации через прямые SQL запросы
    """
    try:
        from django.db import connection
        
        with connection.cursor() as cursor:
            # Проверяем, что пользователь существует
            cursor.execute("SELECT id, username, is_superuser FROM auth_user WHERE id = %s", [user_id])
            user_row = cursor.fetchone()
            
            if not user_row:
                return JsonResponse({
                    'success': False,
                    'error': 'Пользователь не найден'
                }, status=404)
            
            user_id_db, username, is_superuser = user_row
            
            # Нельзя удалить суперпользователя
            if is_superuser:
                return JsonResponse({
                    'success': False,
                    'error': 'Нельзя удалить суперпользователя'
                }, status=400)
            
            # Удаляем связанные данные пользователя (если таблицы существуют)
            try:
                # Удаляем профиль пользователя
                cursor.execute("DELETE FROM accounts_userprofile WHERE user_id = %s", [user_id])
            except Exception:
                pass  # Таблица может не существовать
            
            try:
                # Удаляем группы пользователя (если таблица существует)
                cursor.execute("DELETE FROM auth_user_groups WHERE user_id = %s", [user_id])
            except Exception:
                pass  # Таблица может не существовать
            
            try:
                # Удаляем права пользователя (если таблица существует)
                cursor.execute("DELETE FROM auth_user_user_permissions WHERE user_id = %s", [user_id])
            except Exception:
                pass  # Таблица может не существовать
            
            # Удаляем самого пользователя
            cursor.execute("DELETE FROM auth_user WHERE id = %s", [user_id])
            
            # Проверяем, что пользователь действительно удален
            cursor.execute("SELECT COUNT(*) FROM auth_user WHERE id = %s", [user_id])
            remaining_count = cursor.fetchone()[0]
            
            if remaining_count > 0:
                return JsonResponse({
                    'success': False,
                    'error': 'Не удалось удалить пользователя'
                }, status=500)
        
        return JsonResponse({
            'success': True,
            'message': f'Пользователь {username} успешно удален'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Ошибка удаления пользователя: {str(e)}'
        }, status=500)


@csrf_exempt
@require_http_methods(["PUT"])
def simple_update_user(request, user_id):
    """
    Обновление пользователя без аутентификации
    """
    try:
        from django.contrib.auth.models import User
        from accounts.models import UserProfile
        import json
        
        # Получаем данные из запроса
        data = json.loads(request.body)
        
        # Проверяем, что пользователь существует
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Пользователь не найден'
            }, status=404)
        
        # Обновляем основные данные пользователя
        if 'username' in data:
            user.username = data['username']
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'email' in data:
            user.email = data['email']
        if 'is_active' in data:
            user.is_active = data['is_active']
        
        user.save()
        
        # Получаем или создаем профиль пользователя
        profile, created = UserProfile.objects.get_or_create(
            user=user,
            defaults={
                'role': 'user',
                'phone': '',
                'department': '',
                'is_active_user': True
            }
        )
        
        # Обновляем данные профиля
        if 'role' in data:
            profile.role = data['role']
        if 'phone' in data:
            profile.phone = data['phone']
        if 'department' in data:
            profile.department = data['department']
        if 'is_active_user' in data:
            profile.is_active_user = data['is_active_user']
        
        profile.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Пользователь {user.username} успешно обновлен',
            'user': {
                'id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'is_active': user.is_active,
                'role': profile.role,
                'phone': profile.phone or '',
                'department': profile.department or '',
                'is_active_user': profile.is_active_user,
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Ошибка обновления пользователя: {str(e)}'
        }, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def simple_database_status(request):
    """
    Простая проверка состояния базы данных без аутентификации
    """
    try:
        from django.db import connection
        from django.contrib.auth.models import User
        from accounts.models import UserProfile
        
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
        user_count = User.objects.count() if auth_user_exists else 0
        profile_count = UserProfile.objects.count() if userprofile_exists else 0
        
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
def simple_force_initialize_database(request):
    """
    Простая принудительная инициализация базы данных без аутентификации
    """
    try:
        from django.core.management import call_command
        from django.db import connection
        from django.contrib.auth.models import User
        from accounts.models import UserProfile
        from django.contrib.auth.hashers import make_password
        from django.utils import timezone
        import logging
        
        logger = logging.getLogger(__name__)
        
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
        }, status=200)
        
    except Exception as e:
        error_msg = f'Критическая ошибка инициализации базы данных: {str(e)}'
        logger.error(error_msg)
        return JsonResponse({
            'success': False,
            'error': error_msg
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def simple_create_user(request):
    """
    Простое создание пользователя без аутентификации
    """
    try:
        from django.contrib.auth.models import User
        from accounts.models import UserProfile
        from django.contrib.auth.hashers import make_password
        from django.utils import timezone
        import json
        
        # Get form data - handle both POST and JSON
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            role = data.get('role', 'user')
            email = data.get('email', '')
            first_name = data.get('first_name', '')
            last_name = data.get('last_name', '')
            phone = data.get('phone', '')
            department = data.get('department', '')
        else:
            username = request.POST.get('username')
            password = request.POST.get('password')
            role = request.POST.get('role', 'user')
            email = request.POST.get('email', '')
            first_name = request.POST.get('first_name', '')
            last_name = request.POST.get('last_name', '')
            phone = request.POST.get('phone', '')
            department = request.POST.get('department', '')
        
        # Debug logging
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f'Create user request - Content-Type: {request.content_type}')
        logger.info(f'Create user data - username: {username}, password: {"***" if password else "None"}')
        
        if not username or not password:
            return JsonResponse({
                'success': False,
                'error': f'Имя пользователя и пароль обязательны. Получено: username="{username}", password={"***" if password else "None"}"'
            }, status=400)
        
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                'success': False,
                'error': 'Пользователь с таким именем уже существует'
            }, status=400)
        
        # Create user
        user = User.objects.create(
            username=username,
            password=make_password(password),
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_active=True,
            date_joined=timezone.now()
        )
        
        # Create profile
        profile = UserProfile.objects.create(
            user=user,
            role=role,
            phone=phone,
            department=department,
            is_active_user=True,
            created_at=timezone.now(),
            updated_at=timezone.now()
        )
        
        return JsonResponse({
            'success': True,
            'message': f'Пользователь {username} успешно создан',
            'user_id': user.id
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Ошибка создания пользователя: {str(e)}'
        }, status=500)
