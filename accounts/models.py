from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Кастомная модель пользователя с ролями
    """
    ROLE_CHOICES = [
        ('admin', 'Администратор'),
        ('management', 'Руководство'),
    ]
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='management',
        verbose_name='Роль'
    )
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    department = models.CharField(max_length=100, blank=True, verbose_name='Отдел')
    
    def is_admin(self):
        return self.role == 'admin'
    
    def is_management(self):
        return self.role == 'management'
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

