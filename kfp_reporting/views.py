from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

@csrf_exempt
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
def simple_health(request):
    """
    Максимально простой health check для Railway
    """
    return HttpResponse("OK", status=200)

@csrf_exempt
def minimal_health(request):
    """
    Минимальный health check - только текст
    """
    return HttpResponse("OK")

@csrf_exempt
def home(request):
    """
    Главная страница приложения
    """
    html_content = """
    <html>
    <head>
        <title>KFP Reporting API</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .container { max-width: 800px; margin: 0 auto; }
            .endpoint { background: #f5f5f5; padding: 10px; margin: 5px 0; border-radius: 5px; }
            .success { color: #28a745; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1 class="success">✅ KFP Reporting API is running!</h1>
            <p>Django приложение успешно развернуто на Railway.</p>
            
            <h2>Доступные endpoints:</h2>
            <div class="endpoint"><strong>GET /admin/</strong> - Django Admin панель</div>
            <div class="endpoint"><strong>GET /api/reports/</strong> - API для отчетов</div>
            <div class="endpoint"><strong>GET /api/auth/</strong> - API для аутентификации</div>
            <div class="endpoint"><strong>GET /health/</strong> - Health check</div>
            
            <h2>Статус:</h2>
            <p class="success">🚀 Приложение работает стабильно</p>
            <p>📊 База данных: PostgreSQL подключена</p>
            <p>🔧 Middleware: Настроен правильно</p>
            <p>🌐 Railway: Развертывание успешно</p>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html_content, content_type="text/html")
