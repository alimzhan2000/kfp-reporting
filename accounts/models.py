"""
Модели для системы управления пользователями
"""
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator

class UserProfile(models.Model):
    """Профиль пользователя для расширения стандартной модели User"""
    ROLES = [
        ('admin', 'Администратор'),
        ('manager', 'Менеджер'),
        ('user', 'Пользователь'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(
        max_length=20,
        choices=ROLES,
        default='user',
        verbose_name='Роль'
    )
    
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Телефон'
    )
    
    department = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Отдел'
    )
    
    is_active_user = models.BooleanField(
        default=True,
        verbose_name='Активный пользователь'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )
    
    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"
    
    def get_full_name(self):
        return f"{self.user.first_name} {self.user.last_name}".strip() or self.user.username