from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class DataUpload(models.Model):
    """
    Модель для отслеживания загруженных файлов
    """
    STATUS_CHOICES = [
        ('pending', 'Ожидает обработки'),
        ('processing', 'Обрабатывается'),
        ('completed', 'Завершено'),
        ('failed', 'Ошибка'),
    ]
    
    file_name = models.CharField(max_length=255, verbose_name='Имя файла')
    file_path = models.CharField(max_length=500, verbose_name='Путь к файлу')
    file_size = models.BigIntegerField(verbose_name='Размер файла (байт)')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Статус')
    records_processed = models.IntegerField(default=0, verbose_name='Обработано записей')
    records_created = models.IntegerField(default=0, verbose_name='Создано записей')
    records_updated = models.IntegerField(default=0, verbose_name='Обновлено записей')
    error_message = models.TextField(blank=True, verbose_name='Сообщение об ошибке')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Загружено пользователем')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата загрузки')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='Дата завершения')
    
    class Meta:
        verbose_name = 'Загрузка данных'
        verbose_name_plural = 'Загрузки данных'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.file_name} ({self.get_status_display()})"

