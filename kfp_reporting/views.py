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
    Главная страница - показывает KFP Reporting dashboard
    """
    try:
        # Пытаемся найти index.html из static
        from django.conf import settings
        from pathlib import Path
        
        static_index_path = settings.BASE_DIR / 'static' / 'index.html'
        
        if static_index_path.exists():
            with open(static_index_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            return HttpResponse(html_content, content_type="text/html")
        else:
            # Fallback - показываем простую страницу с инструкциями
            return render_react_setup_page()
            
    except Exception as e:
        # Если что-то пошло не так, показываем инструкции
        return render_react_setup_page()

def render_react_setup_page():
    """Показывает страницу с инструкциями по сборке React"""
    html_content = """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>KFP Reporting - Настройка Frontend</title>
        <style>
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                margin: 0; 
                padding: 20px; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }
            .container { 
                max-width: 800px; 
                margin: 0 auto; 
                background: white;
                border-radius: 15px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                overflow: hidden;
            }
            .header {
                background: linear-gradient(135deg, #28a745, #20c997);
                color: white;
                padding: 30px;
                text-align: center;
            }
            .content { padding: 40px; }
            .code {
                background: #f8f9fa;
                padding: 15px;
                border-radius: 8px;
                font-family: monospace;
                margin: 10px 0;
                border-left: 4px solid #007bff;
            }
            .btn {
                display: inline-block;
                padding: 12px 24px;
                margin: 10px 5px;
                background: #007bff;
                color: white;
                text-decoration: none;
                border-radius: 6px;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🌾 KFP Reporting</h1>
                <p>Настройка Frontend приложения</p>
            </div>
            
            <div class="content">
                <h2>📱 Для запуска React Frontend:</h2>
                
                <p>1. Перейдите в папку frontend:</p>
                <div class="code">cd frontend</div>
                
                <p>2. Установите зависимости:</p>
                <div class="code">npm install</div>
                
                <p>3. Соберите приложение для production:</p>
                <div class="code">npm run build</div>
                
                <p>4. Перезапустите Django сервер</p>
                
                <h3>🔗 Альтернативные ссылки:</h3>
                <a href="/admin/" class="btn">🔐 Admin Panel</a>
                <a href="/api/reports/data/" class="btn">📊 API Data</a>
                <a href="/health/" class="btn">❤️ Health Check</a>
                
                <h3>🌐 API Endpoints:</h3>
                <ul>
                    <li><strong>GET /api/reports/data/</strong> - Сельскохозяйственные данные</li>
                    <li><strong>GET /api/reports/yield-comparison/</strong> - Сравнение урожайности</li>
                    <li><strong>GET /api/reports/field-efficiency/</strong> - Эффективность полей</li>
                    <li><strong>POST /api/upload/</strong> - Загрузка данных</li>
                </ul>
            </div>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html_content, content_type="text/html")
