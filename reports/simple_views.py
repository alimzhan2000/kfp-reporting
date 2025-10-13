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
