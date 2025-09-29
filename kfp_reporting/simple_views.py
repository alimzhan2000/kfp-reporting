from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

@csrf_exempt
@require_http_methods(["GET"])
def health_check(request):
    """
    Простейшая проверка здоровья без зависимостей от базы данных
    """
    return JsonResponse({
        'status': 'ok',
        'message': 'KFP Reporting API is running',
        'version': '1.0.0'
    })

@csrf_exempt
@require_http_methods(["GET"])
def home(request):
    """
    Главная страница без зависимостей
    """
    return JsonResponse({
        'message': 'KFP Reporting System',
        'status': 'running',
        'api_endpoints': {
            'health': '/api/health/',
            'dashboard': '/api/reports/dashboard-stats/',
            'upload': '/api/upload/file/',
            'reports': '/api/reports/',
            'admin': '/admin/'
        }
    })
