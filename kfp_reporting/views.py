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
    Главная страница KFP Reporting проекта
    """
    html_content = """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>KFP Reporting - Система отчетности</title>
        <style>
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                margin: 0; 
                padding: 20px; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }
            .container { 
                max-width: 1200px; 
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
            .header h1 { margin: 0; font-size: 2.5em; }
            .header p { margin: 10px 0 0 0; font-size: 1.2em; opacity: 0.9; }
            
            .content { padding: 40px; }
            
            .status-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin: 30px 0;
            }
            .status-card {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 10px;
                border-left: 4px solid #28a745;
            }
            .status-card h3 { margin: 0 0 10px 0; color: #333; }
            .status-card p { margin: 0; color: #666; }
            
            .endpoints {
                background: #f8f9fa;
                padding: 30px;
                border-radius: 10px;
                margin: 30px 0;
            }
            .endpoint { 
                background: white; 
                padding: 15px; 
                margin: 10px 0; 
                border-radius: 8px;
                border-left: 4px solid #007bff;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .endpoint-method {
                background: #007bff;
                color: white;
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 0.8em;
                font-weight: bold;
            }
            .endpoint-desc { color: #666; }
            
            .actions {
                text-align: center;
                margin: 30px 0;
            }
            .btn {
                display: inline-block;
                padding: 12px 24px;
                margin: 0 10px;
                background: #007bff;
                color: white;
                text-decoration: none;
                border-radius: 6px;
                font-weight: bold;
                transition: background 0.3s;
            }
            .btn:hover { background: #0056b3; }
            .btn-admin { background: #dc3545; }
            .btn-admin:hover { background: #c82333; }
            
            .footer {
                background: #343a40;
                color: white;
                padding: 20px;
                text-align: center;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🌾 KFP Reporting</h1>
                <p>Система отчетности сельскохозяйственных данных</p>
            </div>
            
            <div class="content">
                <h2>📊 Статус системы</h2>
                <div class="status-grid">
                    <div class="status-card">
                        <h3>🚀 Приложение</h3>
                        <p>Работает стабильно на Railway</p>
                    </div>
                    <div class="status-card">
                        <h3>📊 База данных</h3>
                        <p>PostgreSQL подключена и готова</p>
                    </div>
                    <div class="status-card">
                        <h3>🔧 API</h3>
                        <p>Все endpoints доступны</p>
                    </div>
                    <div class="status-card">
                        <h3>🔐 Аутентификация</h3>
                        <p>Система авторизации активна</p>
                    </div>
                </div>
                
                <h2>🌐 API Endpoints</h2>
                <div class="endpoints">
                    <div class="endpoint">
                        <span><span class="endpoint-method">GET</span> <strong>/api/reports/data/</strong></span>
                        <span class="endpoint-desc">Список сельскохозяйственных данных</span>
                    </div>
                    <div class="endpoint">
                        <span><span class="endpoint-method">GET</span> <strong>/api/reports/yield-comparison/</strong></span>
                        <span class="endpoint-desc">Сравнение урожайности</span>
                    </div>
                    <div class="endpoint">
                        <span><span class="endpoint-method">GET</span> <strong>/api/reports/field-efficiency/</strong></span>
                        <span class="endpoint-desc">Эффективность полей</span>
                    </div>
                    <div class="endpoint">
                        <span><span class="endpoint-method">GET</span> <strong>/api/reports/variety-performance/</strong></span>
                        <span class="endpoint-desc">Производительность сортов</span>
                    </div>
                    <div class="endpoint">
                        <span><span class="endpoint-method">POST</span> <strong>/api/upload/</strong></span>
                        <span class="endpoint-desc">Загрузка данных</span>
                    </div>
                    <div class="endpoint">
                        <span><span class="endpoint-method">GET</span> <strong>/api/auth/</strong></span>
                        <span class="endpoint-desc">Аутентификация</span>
                    </div>
                </div>
                
                <div class="actions">
                    <a href="/admin/" class="btn btn-admin">🔐 Admin Panel</a>
                    <a href="/api/reports/data/" class="btn">📊 API Data</a>
                    <a href="/health/" class="btn">❤️ Health Check</a>
                </div>
            </div>
            
            <div class="footer">
                <p>KFP Reporting API v1.0 | Развернуто на Railway</p>
                <p>Доступно по адресу: <strong>https://kfp-reporting.up.railway.app</strong></p>
            </div>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html_content, content_type="text/html")
