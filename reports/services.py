from django.db.models import Avg, Sum, Count, Max, F, ExpressionWrapper, DecimalField
from .models import AgriculturalData


class ReportService:
    """
    Сервис для генерации отчетов
    """
    
    @staticmethod
    def get_yield_comparison_data(filters=None):
        """
        Данные для сравнительного отчета по урожайности
        """
        queryset = AgriculturalData.objects.all()
        
        if filters:
            if filters.get('field_name'):
                queryset = queryset.filter(field_name__icontains=filters['field_name'])
            if filters.get('year_from'):
                queryset = queryset.filter(year__gte=filters['year_from'])
            if filters.get('year_to'):
                queryset = queryset.filter(year__lte=filters['year_to'])
            if filters.get('variety'):
                queryset = queryset.filter(variety__icontains=filters['variety'])
            if filters.get('final_product'):
                queryset = queryset.filter(final_product__icontains=filters['final_product'])
        
        # Группировка по полям
        total_yield_expr = ExpressionWrapper(F('planting_area') * F('yield_per_hectare'), output_field=DecimalField(max_digits=16, decimal_places=2))

        field_data = queryset.values('field_name').annotate(
            avg_yield=Avg('yield_per_hectare'),
            total_area=Sum('planting_area'),
            total_yield=Sum(total_yield_expr),
            product_count=Count('final_product', distinct=True)
        ).order_by('-avg_yield')
        
        # Группировка по годам
        year_data = queryset.values('year').annotate(
            avg_yield=Avg('yield_per_hectare'),
            total_area=Sum('planting_area'),
            total_yield=Sum(total_yield_expr)
        ).order_by('year')
        
        # Группировка по конечному продукту (замена культуры)
        product_data = queryset.values('final_product').annotate(
            avg_yield=Avg('yield_per_hectare'),
            total_area=Sum('planting_area'),
            total_yield=Sum(total_yield_expr),
            variety_count=Count('variety', distinct=True)
        ).order_by('-avg_yield')
        
        # Группировка по сортам в разрезе конечного продукта
        variety_data = queryset.values('variety', 'final_product').annotate(
            avg_yield=Avg('yield_per_hectare'),
            max_yield=Max('yield_per_hectare'),
            total_area=Sum('planting_area'),
            total_yield=Sum(total_yield_expr),
            count=Count('id'),
            fields=Count('field_name', distinct=True)
        ).order_by('final_product', '-avg_yield')
        
        # Подготавливаем данные для фронтенда
        years = [item['year'] for item in year_data]
        yield_by_year = [float(item['avg_yield']) if item['avg_yield'] else 0 for item in year_data]
        
        products = [item['final_product'] for item in product_data]
        yield_by_product = [float(item['avg_yield']) if item['avg_yield'] else 0 for item in product_data]
        
        # Сводная таблица для отчета
        summary = []
        for item in year_data:
            for product_item in product_data:
                # Находим записи для конкретного года и продукта
                year_product_data = queryset.filter(
                    year=item['year'],
                    final_product=product_item['final_product']
                )
                if year_product_data.exists():
                    avg_yield = year_product_data.aggregate(avg=Avg('yield_per_hectare'))['avg']
                    max_yield = year_product_data.aggregate(max=Max('yield_per_hectare'))['max']
                    count = year_product_data.count()
                    
                    summary.append({
                        'year': item['year'],
                        'final_product': product_item['final_product'],
                        'avg_yield': float(avg_yield) if avg_yield else 0,
                        'max_yield': float(max_yield) if max_yield else 0,
                        'count': count
                    })
        
        return {
            'years': years,
            'yield_by_year': yield_by_year,
            'products': products,
            'yield_by_product': yield_by_product,
            'summary': summary,
            'total_records': queryset.count(),
            'field_comparison': list(field_data),
            'year_comparison': list(year_data),
            'product_comparison': list(product_data),
            'variety_comparison': list(variety_data)
        }
    
    @staticmethod
    def get_field_efficiency_data(filters=None):
        """
        Данные для отчета по эффективности полей
        """
        queryset = AgriculturalData.objects.all()
        total_yield_expr = ExpressionWrapper(F('planting_area') * F('yield_per_hectare'), output_field=DecimalField(max_digits=16, decimal_places=2))
        
        if filters:
            if filters.get('year_from'):
                queryset = queryset.filter(year__gte=filters['year_from'])
            if filters.get('year_to'):
                queryset = queryset.filter(year__lte=filters['year_to'])
            if filters.get('final_product'):
                queryset = queryset.filter(final_product__icontains=filters['final_product'])
        
        # Данные по полям с эффективностью
        field_data = queryset.values('field_name').annotate(
            avg_yield=Avg('yield_per_hectare'),
            total_area=Sum('planting_area'),
            total_yield=Sum(total_yield_expr),
            product_count=Count('final_product', distinct=True),
            year_count=Count('year', distinct=True),
            record_count=Count('id')
        ).order_by('-avg_yield')
        
        # Статистика для определения цветовых градаций
        yields = [float(item['avg_yield']) for item in field_data if item['avg_yield'] is not None]
        if yields:
            min_yield = min(yields)
            max_yield = max(yields)
            avg_yield = sum(yields) / len(yields)
        else:
            min_yield = max_yield = avg_yield = 0
        
        # Добавляем цветовые категории
        for item in field_data:
            yield_value = float(item['avg_yield'] or 0)
            if yield_value >= max_yield * 0.8:
                item['efficiency_level'] = 'high'
                item['color'] = '#22c55e'  # зеленый
            elif yield_value >= avg_yield:
                item['efficiency_level'] = 'medium'
                item['color'] = '#eab308'  # желтый
            else:
                item['efficiency_level'] = 'low'
                item['color'] = '#ef4444'  # красный
        
        # Подготавливаем данные для фронтенда
        field_names = [item['field_name'] for item in field_data]
        yields = [float(item['avg_yield']) if item['avg_yield'] else 0 for item in field_data]
        colors = [item['color'] for item in field_data]
        
        # Scatter plot data (area vs yield)
        scatter_data = []
        for item in field_data:
            if item['total_area'] and item['avg_yield']:
                scatter_data.append({
                    'x': float(item['total_area']),
                    'y': float(item['avg_yield'])
                })
        
        # Years and products for filters
        years = list(queryset.values_list('year', flat=True).distinct().order_by('year'))
        products = list(queryset.values_list('final_product', flat=True).distinct())
        
        return {
            'field_data': list(field_data),
            'field_names': field_names,
            'yields': yields,
            'colors': colors,
            'scatter_data': scatter_data,
            'years': years,
            'products': products,
            'statistics': {
                'min_yield': min_yield,
                'max_yield': max_yield,
                'avg_yield': avg_yield,
                'total_fields': len(field_data)
            }
        }
    
    @staticmethod
    def get_variety_performance_data(filters=None):
        """
        Данные для отчета по производительности сортов
        """
        queryset = AgriculturalData.objects.all()
        
        if filters:
            if filters.get('final_product'):
                queryset = queryset.filter(final_product__icontains=filters['final_product'])
            if filters.get('year_from'):
                queryset = queryset.filter(year__gte=filters['year_from'])
            if filters.get('year_to'):
                queryset = queryset.filter(year__lte=filters['year_to'])
            if filters.get('field_name'):
                queryset = queryset.filter(field_name__icontains=filters['field_name'])
        
        # Группировка по конечному продукту и сортам
        variety_data = queryset.values('final_product', 'variety').annotate(
            avg_yield=Avg('yield_per_hectare'),
            max_yield=Max('yield_per_hectare'),
            total_area=Sum('planting_area'),
            total_yield=Sum('planting_area') * Avg('yield_per_hectare'),
            fields=Count('field_name', distinct=True),
            year_count=Count('year', distinct=True),
            count=Count('id')
        ).order_by('-avg_yield')
        
        # Группировка по конечному продукту для сравнения
        product_summary = queryset.values('final_product').annotate(
            avg_yield=Avg('yield_per_hectare'),
            variety_count=Count('variety', distinct=True),
            total_area=Sum('planting_area')
        ).order_by('-avg_yield')
        
        # Статистика по сортам в рамках каждой культуры
        product_variety_stats = {}
        for prod in product_summary:
            prod_name = prod['final_product']
            prod_varieties = [item for item in variety_data if item['final_product'] == prod_name]
            if prod_varieties:
                prod_yields = [v['avg_yield'] for v in prod_varieties if v['avg_yield']]
                if prod_yields:
                    product_variety_stats[prod_name] = {
                        'min_yield': min(prod_yields),
                        'max_yield': max(prod_yields),
                        'avg_yield': sum(prod_yields) / len(prod_yields),
                        'variety_count': len(prod_varieties)
                    }
        
        # Подготавливаем данные для фронтенда
        variety_names = [f"{item['variety']} ({item['final_product']})" for item in variety_data]
        variety_yields = [float(item['avg_yield']) if item['avg_yield'] else 0 for item in variety_data]
        
        # Product distribution data
        product_labels = [item['final_product'] for item in product_summary]
        product_data = [item['variety_count'] for item in product_summary]
        
        # Years and products for filters
        years = list(queryset.values_list('year', flat=True).distinct().order_by('year'))
        products = list(queryset.values_list('final_product', flat=True).distinct())
        
        return {
            'variety_data': list(variety_data),
            'variety_names': variety_names,
            'variety_yields': variety_yields,
            'product_labels': product_labels,
            'product_data': product_data,
            'years': years,
            'products': products,
            'product_summary': list(product_summary),
            'product_variety_stats': product_variety_stats,
            'total_records': queryset.count()
        }

