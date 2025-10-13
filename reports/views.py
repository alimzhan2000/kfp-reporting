from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend  # Восстановлено
from rest_framework import filters
from rest_framework.generics import ListAPIView
from django.db.models import Avg, Sum
from django.utils import timezone
from .models import AgriculturalData, ReportTemplate
from .serializers import AgriculturalDataSerializer, ReportTemplateSerializer
from .services import ReportService


class AgriculturalDataListView(ListAPIView):
    """
    Список сельскохозяйственных данных с фильтрацией
    """
    queryset = AgriculturalData.objects.all()
    serializer_class = AgriculturalDataSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]  # Восстановлено
    filterset_fields = ['field_name', 'year', 'variety', 'final_product']  # Восстановлено
    search_fields = ['field_name', 'variety', 'final_product']
    ordering_fields = ['year', 'yield_per_hectare', 'planting_area', 'created_at']
    ordering = ['-year', 'field_name']


@api_view(['GET'])
def yield_comparison_report(request):
    """
    Сравнительный отчет по урожайности
    """
    filters = {
        'field_name': request.GET.get('field_name'),
        'year_from': request.GET.get('year_from'),
        'year_to': request.GET.get('year_to'),
        'final_product': request.GET.get('final_product'),
        'variety': request.GET.get('variety'),
    }
    
    # Убираем None значения
    filters = {k: v for k, v in filters.items() if v is not None}
    
    try:
        data = ReportService.get_yield_comparison_data(filters)
        return Response(data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {'error': f'Ошибка генерации отчета: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def field_efficiency_report(request):
    """
    Отчет по эффективности полей
    """
    filters = {
        'year_from': request.GET.get('year_from'),
        'year_to': request.GET.get('year_to'),
        'final_product': request.GET.get('final_product'),
    }
    
    # Убираем None значения
    filters = {k: v for k, v in filters.items() if v is not None}
    
    try:
        data = ReportService.get_field_efficiency_data(filters)
        return Response(data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {'error': f'Ошибка генерации отчета: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def variety_performance_report(request):
    """
    Отчет по производительности сортов
    """
    filters = {
        'final_product': request.GET.get('final_product'),
        'year_from': request.GET.get('year_from'),
        'year_to': request.GET.get('year_to'),
        'field_name': request.GET.get('field_name'),
    }
    
    # Убираем None значения
    filters = {k: v for k, v in filters.items() if v is not None}
    
    try:
        data = ReportService.get_variety_performance_data(filters)
        return Response(data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {'error': f'Ошибка генерации отчета: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def report_templates(request):
    """
    Список шаблонов отчетов
    """
    templates = ReportTemplate.objects.filter(is_active=True)
    serializer = ReportTemplateSerializer(templates, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def dashboard_stats(request):
    """
    Статистика для дашборда
    """
    try:
        # Добавляем логирование для отладки
        import logging
        logger = logging.getLogger(__name__)
        logger.info('Dashboard stats API called')
        
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
        
        result = {
            'total_records': total_records,
            'unique_fields': unique_fields,
            'unique_products': unique_products,
            'unique_varieties': unique_varieties,
            'latest_year': latest_year,
            'avg_yield': round(avg_yield, 2),
            'total_area': round(total_area, 2)
        }
        
        logger.info(f'Dashboard stats result: {result}')
        return Response(result, status=status.HTTP_200_OK)
        
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f'Dashboard stats error: {str(e)}')
        return Response(
            {'error': f'Ошибка получения статистики: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def simple_test(request):
    """
    Простой тест API без аутентификации
    """
    return Response({
        'message': 'API работает!',
        'status': 'success',
        'timestamp': timezone.now().isoformat()
    }, status=status.HTTP_200_OK)
