"""
Management command для инициализации базы данных
"""
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth.models import User
from accounts.models import UserProfile
from django.contrib.auth.hashers import make_password
from django.utils import timezone


class Command(BaseCommand):
    help = 'Инициализация базы данных и создание демо-пользователей'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Принудительно создать демо-пользователей даже если они уже существуют',
        )

    def handle(self, *args, **options):
        self.stdout.write('🔧 Инициализация базы данных...')
        
        # Применяем все миграции
        self.stdout.write('📦 Применение миграций...')
        try:
            call_command('migrate', verbosity=0)
            self.stdout.write(
                self.style.SUCCESS('✅ Миграции применены успешно')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Ошибка применения миграций: {e}')
            )
            return False
        
        # Создаем демо-пользователей
        self.stdout.write('👥 Создание демо-пользователей...')
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
            try:
                # Проверяем, существует ли пользователь
                if not options['force'] and User.objects.filter(username=user_data['username']).exists():
                    self.stdout.write(
                        self.style.WARNING(f'ℹ️  Пользователь {user_data["username"]} уже существует')
                    )
                    continue
                
                # Удаляем существующего пользователя если force=True
                if options['force'] and User.objects.filter(username=user_data['username']).exists():
                    User.objects.filter(username=user_data['username']).delete()
                
                # Создаем пользователя
                user = User.objects.create(
                    username=user_data['username'],
                    password=make_password(user_data['password']),
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                    email=user_data['email'],
                    is_active=True,
                    date_joined=timezone.now()
                )
                
                # Создаем профиль
                UserProfile.objects.create(
                    user=user,
                    role=user_data['role'],
                    phone=user_data['phone'],
                    department=user_data['department'],
                    is_active_user=user_data['is_active_user'],
                    created_at=timezone.now(),
                    updated_at=timezone.now()
                )
                
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Создан пользователь: {user_data["username"]}')
                )
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'❌ Ошибка создания пользователя {user_data["username"]}: {e}')
                )
        
        print('🎉 Инициализация завершена! Создано пользователей: ' + str(created_count))
        
        # Показываем информацию о базе данных
        user_count = User.objects.count()
        profile_count = UserProfile.objects.count()
        print('📊 Статистика: ' + str(user_count) + ' пользователей, ' + str(profile_count) + ' профилей')
        
        return True
