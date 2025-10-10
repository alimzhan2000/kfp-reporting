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
    # Встроенный HTML dashboard
    html_content = """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>KFP Reporting - Дашборд</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-50">
        <!-- Header -->
        <nav class="bg-white shadow">
            <div class="max-w-7xl mx-auto px-4">
                <div class="flex justify-between items-center py-4">
                    <div class="flex items-center">
                        <div class="text-2xl mr-3">🌾</div>
                        <h1 class="text-gray-900 text-xl font-bold">KFP Reporting</h1>
                    </div>
                    <div class="flex items-center space-x-4">
                        <a href="/admin/" class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded">Admin</a>
                        <a href="/api/reports/data/" class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded">API</a>
                    </div>
                </div>
            </div>
        </nav>

        <!-- Main Content -->
        <div class="max-w-7xl mx-auto px-4 py-8 space-y-6">
            <!-- Header -->
            <div>
                <h1 class="text-2xl font-bold text-gray-900">Дашборд</h1>
                <p class="mt-1 text-sm text-gray-500">
                    Обзор сельскохозяйственных данных и отчетов
                </p>
            </div>

            <!-- Stats Cards -->
            <div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
                <!-- Всего записей -->
                <div class="relative bg-white pt-5 px-4 pb-12 sm:pt-6 sm:px-6 shadow rounded-lg overflow-hidden cursor-pointer hover:shadow-md transition-shadow" onclick="window.location.href='/api/reports/data/'">
                    <dt>
                        <div class="absolute bg-blue-500 rounded-md p-3">
                            <svg class="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                            </svg>
                        </div>
                        <p class="ml-16 text-sm font-medium text-gray-500 truncate">
                            Всего записей
                        </p>
                    </dt>
                    <dd class="ml-16 pb-6 flex items-baseline sm:pb-7">
                        <p class="text-2xl font-semibold text-gray-900" id="total-records">0</p>
                    </dd>
                </div>

                <!-- Количество полей -->
                <div class="relative bg-white pt-5 px-4 pb-12 sm:pt-6 sm:px-6 shadow rounded-lg overflow-hidden cursor-pointer hover:shadow-md transition-shadow" onclick="window.location.href='/api/reports/field-efficiency/'">
                    <dt>
                        <div class="absolute bg-green-500 rounded-md p-3">
                            <svg class="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
                            </svg>
                        </div>
                        <p class="ml-16 text-sm font-medium text-gray-500 truncate">
                            Количество полей
                        </p>
                    </dt>
                    <dd class="ml-16 pb-6 flex items-baseline sm:pb-7">
                        <p class="text-2xl font-semibold text-gray-900" id="unique-fields">0</p>
                    </dd>
                </div>

                <!-- Конечные продукты -->
                <div class="relative bg-white pt-5 px-4 pb-12 sm:pt-6 sm:px-6 shadow rounded-lg overflow-hidden cursor-pointer hover:shadow-md transition-shadow" onclick="window.location.href='/api/reports/variety-performance/'">
                    <dt>
                        <div class="absolute bg-yellow-500 rounded-md p-3">
                            <svg class="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z"></path>
                            </svg>
                        </div>
                        <p class="ml-16 text-sm font-medium text-gray-500 truncate">
                            Конечные продукты
                        </p>
                    </dt>
                    <dd class="ml-16 pb-6 flex items-baseline sm:pb-7">
                        <p class="text-2xl font-semibold text-gray-900" id="unique-products">0</p>
                    </dd>
                </div>

                <!-- Сорта -->
                <div class="relative bg-white pt-5 px-4 pb-12 sm:pt-6 sm:px-6 shadow rounded-lg overflow-hidden cursor-pointer hover:shadow-md transition-shadow" onclick="window.location.href='/api/reports/variety-performance/'">
                    <dt>
                        <div class="absolute bg-purple-500 rounded-md p-3">
                            <svg class="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                            </svg>
                        </div>
                        <p class="ml-16 text-sm font-medium text-gray-500 truncate">
                            Сорта
                        </p>
                    </dt>
                    <dd class="ml-16 pb-6 flex items-baseline sm:pb-7">
                        <p class="text-2xl font-semibold text-gray-900" id="unique-varieties">0</p>
                    </dd>
                </div>
            </div>

            <!-- Quick Actions -->
            <div class="bg-white shadow rounded-lg p-6">
                <h3 class="text-lg font-medium text-gray-900 mb-4">Быстрые действия</h3>
                <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
                    <!-- Загрузить файл -->
                    <div class="relative group bg-white p-6 focus-within:ring-2 focus-within:ring-inset focus-within:ring-blue-500 rounded-lg border border-gray-200 hover:border-gray-300 cursor-pointer transition-colors" onclick="window.location.href='/api/upload/'">
                        <div>
                            <span class="bg-blue-500 rounded-lg inline-flex p-3 ring-4 ring-white">
                                <svg class="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                                </svg>
                            </span>
                        </div>
                        <div class="mt-8">
                            <h3 class="text-lg font-medium">
                                <span class="absolute inset-0"></span>
                                Загрузить файл
                            </h3>
                            <p class="mt-2 text-sm text-gray-500">
                                Загрузить новые данные CSV/XLSX
                            </p>
                        </div>
                    </div>

                    <!-- Сравнительный отчет -->
                    <div class="relative group bg-white p-6 focus-within:ring-2 focus-within:ring-inset focus-within:ring-green-500 rounded-lg border border-gray-200 hover:border-gray-300 cursor-pointer transition-colors" onclick="window.location.href='/api/reports/yield-comparison/'">
                        <div>
                            <span class="bg-green-500 rounded-lg inline-flex p-3 ring-4 ring-white">
                                <svg class="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
                                </svg>
                            </span>
                        </div>
                        <div class="mt-8">
                            <h3 class="text-lg font-medium">
                                <span class="absolute inset-0"></span>
                                Сравнительный отчет
                            </h3>
                            <p class="mt-2 text-sm text-gray-500">
                                Сравнить урожайность по различным параметрам
                            </p>
                        </div>
                    </div>

                    <!-- Эффективность полей -->
                    <div class="relative group bg-white p-6 focus-within:ring-2 focus-within:ring-inset focus-within:ring-blue-500 rounded-lg border border-gray-200 hover:border-gray-300 cursor-pointer transition-colors" onclick="window.location.href='/api/reports/field-efficiency/'">
                        <div>
                            <span class="bg-blue-500 rounded-lg inline-flex p-3 ring-4 ring-white">
                                <svg class="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
                                </svg>
                            </span>
                        </div>
                        <div class="mt-8">
                            <h3 class="text-lg font-medium">
                                <span class="absolute inset-0"></span>
                                Эффективность полей
                            </h3>
                            <p class="mt-2 text-sm text-gray-500">
                                Анализ производительности полей
                            </p>
                        </div>
                    </div>

                    <!-- Производительность сортов -->
                    <div class="relative group bg-white p-6 focus-within:ring-2 focus-within:ring-inset focus-within:ring-purple-500 rounded-lg border border-gray-200 hover:border-gray-300 cursor-pointer transition-colors" onclick="window.location.href='/api/reports/variety-performance/'">
                        <div>
                            <span class="bg-purple-500 rounded-lg inline-flex p-3 ring-4 ring-white">
                                <svg class="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path>
                                </svg>
                            </span>
                        </div>
                        <div class="mt-8">
                            <h3 class="text-lg font-medium">
                                <span class="absolute inset-0"></span>
                                Производительность сортов
                            </h3>
                            <p class="mt-2 text-sm text-gray-500">
                                Сравнение сортов в рамках культур
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <script>
            // Load dashboard data
            async function loadDashboardData() {
                try {
                    const response = await fetch('/api/reports/dashboard-stats/');
                    const data = await response.json();
                    
                    // Update stats
                    document.getElementById('total-records').textContent = data.total_records || 0;
                    document.getElementById('unique-fields').textContent = data.unique_fields || 0;
                    document.getElementById('unique-products').textContent = data.unique_products || 0;
                    document.getElementById('unique-varieties').textContent = data.unique_varieties || 0;
                    
                } catch (error) {
                    console.log('Dashboard data not available yet:', error);
                }
            }

            // Load data on page load
            loadDashboardData();
        </script>
    </body>
    </html>
    """
    return HttpResponse(html_content, content_type="text/html")

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
