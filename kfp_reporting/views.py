from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

@csrf_exempt
@require_http_methods(["GET"])
def health_check(request):
    """
    Простая проверка здоровья приложения для Railway Healthcheck
    """
    return JsonResponse({
        'status': 'ok',
        'message': 'KFP Reporting API is running',
        'version': '1.0.0'
    })

@csrf_exempt
@require_http_methods(["GET"])
def simple_health(request):
    """
    Максимально простой health check для Railway
    """
    from django.http import HttpResponse
    return HttpResponse("OK", status=200)

@csrf_exempt
@require_http_methods(["GET"])
def home(request):
    """
    Главная страница приложения
    """
    # Если это health check запрос, возвращаем простой ответ
    if request.path == '/' and 'health' in request.META.get('HTTP_USER_AGENT', '').lower():
        from django.http import HttpResponse
        return HttpResponse("OK", status=200)
    
    return JsonResponse({
        'message': 'KFP Reporting System',
        'api_endpoints': {
            'health': '/api/health/',
            'simple_health': '/health/',
            'dashboard': '/api/reports/dashboard-stats/',
            'upload': '/api/upload/file/',
            'reports': '/api/reports/',
            'admin': '/admin/'
        },
        'status': 'running'
    })
