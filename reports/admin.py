from django.contrib import admin
from .models import AgriculturalData, ReportTemplate


@admin.register(AgriculturalData)
class AgriculturalDataAdmin(admin.ModelAdmin):
    list_display = ('field_name', 'year', 'crop', 'variety', 'yield_per_hectare', 'planting_area', 'uploaded_by')
    list_filter = ('year', 'crop', 'field_name', 'uploaded_by')
    search_fields = ('field_name', 'crop', 'variety', 'final_product')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('field_name', 'year', 'planting_area', 'yield_per_hectare')
        }),
        ('Детали культуры', {
            'fields': ('crop', 'variety', 'final_product')
        }),
        ('Метаданные', {
            'fields': ('uploaded_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ReportTemplate)
class ReportTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'chart_type', 'is_active', 'created_at')
    list_filter = ('chart_type', 'is_active', 'created_at')
    search_fields = ('name', 'description')

