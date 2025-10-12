from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class AgriculturalData(models.Model):
    """
    Модель для хранения сельскохозяйственных данных
    """
    field_name = models.CharField(max_length=255, verbose_name='Поле')
    year = models.IntegerField(verbose_name='Год')
    planting_area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Площадь посева (га)')
    yield_per_hectare = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Урожайность (ц/га)')
    crop = models.CharField(max_length=255, verbose_name='Культура')
    variety = models.CharField(max_length=255, verbose_name='Сорт')
    final_product = models.CharField(max_length=255, verbose_name='Конечный продукт')
    
    # Дополнительные поля из реального файла
    brigade = models.CharField(max_length=255, blank=True, verbose_name='Бригада')
    field_old_name = models.CharField(max_length=255, blank=True, verbose_name='Поле (старое название)')
    gross_harvest = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True, verbose_name='Валовый сбор (тн)')
    reproduction = models.CharField(max_length=255, blank=True, verbose_name='Репродукция')
    predecessor = models.CharField(max_length=255, blank=True, verbose_name='Предшественник')
    productivity_score = models.IntegerField(null=True, blank=True, verbose_name='Балл продуктивности')
    agro_background = models.CharField(max_length=255, blank=True, verbose_name='Агрофон')
    pzr = models.CharField(max_length=255, blank=True, verbose_name='ПЗР')
    
    # Дополнительные поля для отслеживания
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Загружено пользователем')
    
    class Meta:
        verbose_name = 'Сельскохозяйственные данные'
        verbose_name_plural = 'Сельскохозяйственные данные'
        ordering = ['-year', 'field_name', 'final_product']
        unique_together = ['field_name', 'year', 'final_product', 'variety']
    
    def __str__(self):
        return f"{self.field_name} - {self.final_product} ({self.year})"
    
    @property
    def total_yield(self):
        """Общий урожай в центнерах"""
        return float(self.planting_area) * float(self.yield_per_hectare)


class ReportTemplate(models.Model):
    """
    Модель для шаблонов отчетов
    """
    name = models.CharField(max_length=255, verbose_name='Название отчета')
    description = models.TextField(blank=True, verbose_name='Описание')
    chart_type = models.CharField(max_length=50, verbose_name='Тип графика')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    class Meta:
        verbose_name = 'Шаблон отчета'
        verbose_name_plural = 'Шаблоны отчетов'
    
    def __str__(self):
        return self.name

