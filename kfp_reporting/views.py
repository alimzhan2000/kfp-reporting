from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from auth_required import auth_required
from simple_test_view import simple_test_page
from ultra_simple_view import ultra_simple_test_page
from no_pandas_view import no_pandas_test_page
from basic_python_view import basic_python_test_page
from pandas_isolation_view import pandas_isolation_test_page
from minimal_pandas_view import minimal_pandas_test_page
from original_dashboard import get_original_dashboard
from original_yield_report import get_original_yield_comparison_report
from management_yield_report import get_management_yield_comparison_report
from field_efficiency_report import get_field_efficiency_report
from variety_performance_report import get_variety_performance_report
from login_page import get_login_page
from dashboard_with_auth import get_dashboard_with_auth
from dashboard_improved import get_dashboard_improved
from database_user_management import get_database_user_management_page
from simple_user_management import get_simple_user_management_page
from ultra_simple_user_management import get_ultra_simple_user_management_page
from improved_user_management import get_improved_user_management_page
from init_database_page import get_init_database_page
from simple_init_database import get_simple_init_database_page
from init_database_action import init_database_action
from robust_init_database import get_robust_init_database_page
from robust_init_database_action import robust_init_database_action
from upload_page_with_history import get_upload_page_with_history

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
@auth_required
def home(request):
    """
    Главная страница - показывает KFP Reporting dashboard с авторизацией
    """
    return HttpResponse(get_dashboard_improved(), content_type="text/html")

@csrf_exempt
def login_page(request):
    """
    Страница авторизации
    """
    return HttpResponse(get_login_page(), content_type="text/html")

@csrf_exempt
@auth_required
def user_management_page(request):
    """
    Страница управления пользователями - улучшенная версия с полным функционалом
    """
    return HttpResponse(get_improved_user_management_page(), content_type="text/html")

@csrf_exempt
def init_database_page(request):
    """
    Страница инициализации базы данных - надежная версия
    """
    return HttpResponse(get_robust_init_database_page(), content_type="text/html")

@csrf_exempt
def init_database_action_view(request):
    """
    Действие инициализации базы данных
    """
    return init_database_action(request)

@csrf_exempt
def robust_init_database_action_view(request):
    """
    Надежное действие инициализации базы данных
    """
    return robust_init_database_action(request)

@csrf_exempt
@auth_required
def upload_page_with_history(request):
    """
    Страница загрузки файлов с историей загрузок
    """
    return HttpResponse(get_upload_page_with_history(), content_type="text/html")

@csrf_exempt
def upload_page(request):
    """Страница загрузки файлов"""
    html_content = """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>KFP Reporting - Загрузка файлов</title>
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
                        <a href="/" class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded">Дашборд</a>
                        <a href="/upload/" class="text-blue-600 hover:text-blue-800 px-3 py-2 rounded font-medium">Загрузка</a>
                        <a href="/reports/" class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded">Отчеты</a>
                        <a href="/admin/" class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded">Admin</a>
                    </div>
                </div>
            </div>
        </nav>

        <!-- Main Content -->
        <div class="max-w-4xl mx-auto px-4 py-8">
            <div class="mb-8">
                <h1 class="text-2xl font-bold text-gray-900">Загрузка файлов</h1>
                <p class="mt-1 text-sm text-gray-500">
                    Загрузите CSV или Excel файлы с сельскохозяйственными данными
                </p>
            </div>

            <!-- Upload Area -->
            <div class="bg-white shadow rounded-lg p-8">
                <div id="upload-area" class="border-2 border-dashed border-gray-300 rounded-lg p-12 text-center hover:border-blue-400 transition-colors cursor-pointer">
                    <div class="mx-auto w-12 h-12 text-gray-400 mb-4">
                        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
                        </svg>
                    </div>
                    <h3 class="text-lg font-medium text-gray-900 mb-2">Перетащите файлы сюда</h3>
                    <p class="text-sm text-gray-500 mb-4">или нажмите для выбора файлов</p>
                    <input type="file" id="file-input" class="hidden" accept=".csv,.xlsx,.xls" multiple>
                    <button onclick="document.getElementById('file-input').click()" class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700">
                        Выбрать файлы
                    </button>
                </div>
                
                <!-- Upload Progress -->
                <div id="upload-progress" class="mt-6 hidden">
                    <div class="bg-blue-50 border border-blue-200 rounded-md p-4">
                        <div class="flex items-center">
                            <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600 mr-3"></div>
                            <span class="text-blue-800">Загружается...</span>
                        </div>
                        <div class="mt-2 bg-gray-200 rounded-full h-2">
                            <div id="progress-bar" class="bg-blue-600 h-2 rounded-full transition-all duration-300" style="width: 0%"></div>
                        </div>
                    </div>
                </div>

                <!-- Upload Result -->
                <div id="upload-result" class="mt-6 hidden">
                    <div class="bg-green-50 border border-green-200 rounded-md p-4">
                        <div class="flex items-center">
                            <svg class="h-5 w-5 text-green-400 mr-2" fill="currentColor" viewBox="0 0 20 20">
                                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                            </svg>
                            <span class="text-green-800 font-medium">Файл успешно загружен!</span>
                        </div>
                        <p id="result-message" class="text-green-700 text-sm mt-1"></p>
                    </div>
                </div>

                <!-- Error Result -->
                <div id="upload-error" class="mt-6 hidden">
                    <div class="bg-red-50 border border-red-200 rounded-md p-4">
                        <div class="flex items-center">
                            <svg class="h-5 w-5 text-red-400 mr-2" fill="currentColor" viewBox="0 0 20 20">
                                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
                            </svg>
                            <span class="text-red-800 font-medium">Ошибка загрузки</span>
                        </div>
                        <p id="error-message" class="text-red-700 text-sm mt-1"></p>
                    </div>
                </div>
            </div>

            <!-- Instructions -->
            <div class="mt-8 bg-white shadow rounded-lg p-6">
                <h3 class="text-lg font-medium text-gray-900 mb-4">Инструкции по загрузке</h3>
                <div class="space-y-3 text-sm text-gray-600">
                    <p>• Поддерживаемые форматы: CSV, XLSX, XLS</p>
                    <p>• Файл должен содержать колонки: Поле, Год, Площадь посева, Урожайность, Культура, Сорт, Конечный продукт</p>
                    <p>• Максимальный размер файла: 10 MB</p>
                    <p>• После загрузки данные будут автоматически обработаны и добавлены в систему</p>
                </div>
            </div>
        </div>

        <script>
            const uploadArea = document.getElementById('upload-area');
            const fileInput = document.getElementById('file-input');
            const progressDiv = document.getElementById('upload-progress');
            const resultDiv = document.getElementById('upload-result');
            const errorDiv = document.getElementById('upload-error');
            const progressBar = document.getElementById('progress-bar');

            // Drag and drop handlers
            uploadArea.addEventListener('dragover', (e) => {
                e.preventDefault();
                uploadArea.classList.add('border-blue-400', 'bg-blue-50');
            });

            uploadArea.addEventListener('dragleave', (e) => {
                e.preventDefault();
                uploadArea.classList.remove('border-blue-400', 'bg-blue-50');
            });

            uploadArea.addEventListener('drop', (e) => {
                e.preventDefault();
                uploadArea.classList.remove('border-blue-400', 'bg-blue-50');
                const files = e.dataTransfer.files;
                if (files.length > 0) {
                    handleFileUpload(files[0]);
                }
            });

            // File input handler
            fileInput.addEventListener('change', (e) => {
                if (e.target.files.length > 0) {
                    handleFileUpload(e.target.files[0]);
                }
            });

            // Upload function
            async function handleFileUpload(file) {
                const formData = new FormData();
                formData.append('file', file);

                // Show progress
                progressDiv.classList.remove('hidden');
                resultDiv.classList.add('hidden');
                errorDiv.classList.add('hidden');

                try {
                    const response = await fetch('/api/upload/', {
                        method: 'POST',
                        body: formData
                    });

                    if (response.ok) {
                        const result = await response.json();
                        progressDiv.classList.add('hidden');
                        resultDiv.classList.remove('hidden');
                        document.getElementById('result-message').textContent = 
                            `Обработано ${result.upload?.records_processed || 0} записей. Создано: ${result.upload?.records_created || 0}, Обновлено: ${result.upload?.records_updated || 0}`;
                    } else {
                        const errorData = await response.json();
                        throw new Error(errorData.error || 'Ошибка загрузки файла');
                    }
                } catch (error) {
                    progressDiv.classList.add('hidden');
                    errorDiv.classList.remove('hidden');
                    document.getElementById('error-message').textContent = error.message;
                }
            }

            // Simulate progress
            function simulateProgress() {
                let width = 0;
                const interval = setInterval(() => {
                    width += 10;
                    progressBar.style.width = width + '%';
                    if (width >= 100) {
                        clearInterval(interval);
                    }
                }, 200);
            }
        </script>
    </body>
    </html>
    """
    return HttpResponse(html_content, content_type="text/html")

@csrf_exempt
def reports_page(request):
    """Страница отчетов"""
    html_content = """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>KFP Reporting - Отчеты</title>
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
                        <a href="/" class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded">Дашборд</a>
                        <a href="/upload/" class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded">Загрузка</a>
                        <a href="/reports/" class="text-blue-600 hover:text-blue-800 px-3 py-2 rounded font-medium">Отчеты</a>
                        <a href="/admin/" class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded">Admin</a>
                    </div>
                </div>
            </div>
        </nav>

        <!-- Main Content -->
        <div class="max-w-7xl mx-auto px-4 py-8">
            <div class="mb-8">
                <h1 class="text-2xl font-bold text-gray-900">Отчеты</h1>
                <p class="mt-1 text-sm text-gray-500">
                    Анализ сельскохозяйственных данных и производительности
                </p>
            </div>

            <!-- Report Cards -->
            <div class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
                <!-- Yield Comparison -->
                <div class="bg-white shadow rounded-lg p-6 cursor-pointer hover:shadow-md transition-shadow" onclick="window.location.href='/reports/yield-comparison/'">
                    <div class="flex items-center mb-4">
                        <div class="bg-green-100 p-3 rounded-lg mr-4">
                            <svg class="h-6 w-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
                            </svg>
                        </div>
                        <h3 class="text-lg font-medium text-gray-900">Сравнение урожайности</h3>
                    </div>
                    <p class="text-gray-600 text-sm">Сравнение урожайности по годам, культурам и сортам</p>
                </div>

                <!-- Field Efficiency -->
                <div class="bg-white shadow rounded-lg p-6 cursor-pointer hover:shadow-md transition-shadow" onclick="window.location.href='/reports/field-efficiency/'">
                    <div class="flex items-center mb-4">
                        <div class="bg-blue-100 p-3 rounded-lg mr-4">
                            <svg class="h-6 w-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
                            </svg>
                        </div>
                        <h3 class="text-lg font-medium text-gray-900">Эффективность полей</h3>
                    </div>
                    <p class="text-gray-600 text-sm">Анализ производительности и эффективности полей</p>
                </div>

                <!-- Variety Performance -->
                <div class="bg-white shadow rounded-lg p-6 cursor-pointer hover:shadow-md transition-shadow" onclick="window.location.href='/reports/variety-performance/'">
                    <div class="flex items-center mb-4">
                        <div class="bg-purple-100 p-3 rounded-lg mr-4">
                            <svg class="h-6 w-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path>
                            </svg>
                        </div>
                        <h3 class="text-lg font-medium text-gray-900">Производительность сортов</h3>
                    </div>
                    <p class="text-gray-600 text-sm">Сравнение производительности различных сортов</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html_content, content_type="text/html")

@csrf_exempt
@auth_required
def yield_comparison_report(request):
    """Отчет сравнения урожайности для менеджмента"""
    return HttpResponse(get_management_yield_comparison_report(), content_type="text/html")

@csrf_exempt
def test_upload_page(request):
    """Тестовая страница загрузки файлов с диагностикой"""
    html_content = """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>KFP Reporting - Тестовая загрузка</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-50">
        <!-- Header -->
        <nav class="bg-white shadow">
            <div class="max-w-7xl mx-auto px-4">
                <div class="flex justify-between items-center py-4">
                    <div class="flex items-center">
                        <div class="text-2xl mr-3">🧪</div>
                        <h1 class="text-gray-900 text-xl font-bold">KFP Reporting - Тестовая загрузка</h1>
                    </div>
                    <div class="flex items-center space-x-4">
                        <a href="/" class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded">Дашборд</a>
                        <a href="/upload/" class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded">Обычная загрузка</a>
                        <a href="/admin/" class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded">Admin</a>
                    </div>
                </div>
            </div>
        </nav>

        <!-- Main Content -->
        <div class="max-w-4xl mx-auto px-4 py-8">
            <div class="mb-8">
                <h1 class="text-2xl font-bold text-gray-900">Тестовая загрузка файлов</h1>
                <p class="mt-1 text-sm text-gray-500">
                    Эта страница предназначена для диагностики проблем с загрузкой файлов
                </p>
            </div>

            <!-- Upload Area -->
            <div class="bg-white shadow rounded-lg p-8">
                <div id="upload-area" class="border-2 border-dashed border-gray-300 rounded-lg p-12 text-center hover:border-blue-400 transition-colors cursor-pointer">
                    <div class="mx-auto w-12 h-12 text-gray-400 mb-4">
                        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
                        </svg>
                    </div>
                    <h3 class="text-lg font-medium text-gray-900 mb-2">Перетащите файлы сюда</h3>
                    <p class="text-sm text-gray-500 mb-4">или нажмите для выбора файлов</p>
                    <input type="file" id="file-input" class="hidden" accept=".csv,.xlsx,.xls" multiple>
                    <button onclick="document.getElementById('file-input').click()" class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700">
                        Выбрать файлы
                    </button>
                </div>
                
                <!-- Upload Progress -->
                <div id="upload-progress" class="mt-6 hidden">
                    <div class="bg-blue-50 border border-blue-200 rounded-md p-4">
                        <div class="flex items-center">
                            <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600 mr-3"></div>
                            <span class="text-blue-800">Загружается...</span>
                        </div>
                        <div class="mt-2 bg-gray-200 rounded-full h-2">
                            <div id="progress-bar" class="bg-blue-600 h-2 rounded-full transition-all duration-300" style="width: 0%"></div>
                        </div>
                    </div>
                </div>

                <!-- Upload Result -->
                <div id="upload-result" class="mt-6 hidden">
                    <div class="bg-green-50 border border-green-200 rounded-md p-4">
                        <div class="flex items-center">
                            <svg class="h-5 w-5 text-green-400 mr-2" fill="currentColor" viewBox="0 0 20 20">
                                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                            </svg>
                            <span class="text-green-800 font-medium">Файл успешно загружен!</span>
                        </div>
                        <p id="result-message" class="text-green-700 text-sm mt-1"></p>
                        <pre id="result-details" class="text-green-700 text-xs mt-2 bg-green-100 p-2 rounded overflow-auto max-h-40"></pre>
                    </div>
                </div>

                <!-- Error Result -->
                <div id="upload-error" class="mt-6 hidden">
                    <div class="bg-red-50 border border-red-200 rounded-md p-4">
                        <div class="flex items-center">
                            <svg class="h-5 w-5 text-red-400 mr-2" fill="currentColor" viewBox="0 0 20 20">
                                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
                            </svg>
                            <span class="text-red-800 font-medium">Ошибка загрузки</span>
                        </div>
                        <p id="error-message" class="text-red-700 text-sm mt-1"></p>
                        <pre id="error-details" class="text-red-700 text-xs mt-2 bg-red-100 p-2 rounded overflow-auto max-h-40"></pre>
                    </div>
                </div>
            </div>

            <!-- Instructions -->
            <div class="mt-8 bg-white shadow rounded-lg p-6">
                <h3 class="text-lg font-medium text-gray-900 mb-4">Инструкции по тестированию</h3>
                <div class="space-y-3 text-sm text-gray-600">
                    <p>• Используется тестовый endpoint /api/upload/test/</p>
                    <p>• Подробные логи будут видны в Railway Dashboard</p>
                    <p>• Поддерживаемые форматы: CSV, XLSX, XLS</p>
                    <p>• Проверьте логи в Railway для диагностики ошибок</p>
                </div>
            </div>
        </div>

        <script>
            const uploadArea = document.getElementById('upload-area');
            const fileInput = document.getElementById('file-input');
            const progressDiv = document.getElementById('upload-progress');
            const resultDiv = document.getElementById('upload-result');
            const errorDiv = document.getElementById('upload-error');
            const progressBar = document.getElementById('progress-bar');

            // Drag and drop handlers
            uploadArea.addEventListener('dragover', (e) => {
                e.preventDefault();
                uploadArea.classList.add('border-blue-400', 'bg-blue-50');
            });

            uploadArea.addEventListener('dragleave', (e) => {
                e.preventDefault();
                uploadArea.classList.remove('border-blue-400', 'bg-blue-50');
            });

            uploadArea.addEventListener('drop', (e) => {
                e.preventDefault();
                uploadArea.classList.remove('border-blue-400', 'bg-blue-50');
                const files = e.dataTransfer.files;
                if (files.length > 0) {
                    handleFileUpload(files[0]);
                }
            });

            // File input handler
            fileInput.addEventListener('change', (e) => {
                if (e.target.files.length > 0) {
                    handleFileUpload(e.target.files[0]);
                }
            });

            // Upload function
            async function handleFileUpload(file) {
                const formData = new FormData();
                formData.append('file', file);

                // Show progress
                progressDiv.classList.remove('hidden');
                resultDiv.classList.add('hidden');
                errorDiv.classList.add('hidden');

                try {
                    console.log('Uploading to test endpoint...');
                    const response = await fetch('/api/upload/test/', {
                        method: 'POST',
                        body: formData
                    });

                    const result = await response.json();
                    console.log('Response:', result);

                    if (response.ok) {
                        progressDiv.classList.add('hidden');
                        resultDiv.classList.remove('hidden');
                        document.getElementById('result-message').textContent = 
                            `Обработано ${result.upload?.records_processed || 0} записей`;
                        document.getElementById('result-details').textContent = JSON.stringify(result, null, 2);
                    } else {
                        throw new Error(result.error || 'Ошибка загрузки файла');
                    }
                } catch (error) {
                    progressDiv.classList.add('hidden');
                    errorDiv.classList.remove('hidden');
                    document.getElementById('error-message').textContent = error.message;
                    document.getElementById('error-details').textContent = error.stack || 'No additional details';
                    console.error('Upload error:', error);
                }
            }

            // Simulate progress
            function simulateProgress() {
                let width = 0;
                const interval = setInterval(() => {
                    width += 10;
                    progressBar.style.width = width + '%';
                    if (width >= 100) {
                        clearInterval(interval);
                    }
                }, 200);
            }
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

@csrf_exempt
def field_efficiency_report(request):
    """Отчет эффективности полей для менеджмента"""
    return HttpResponse(get_field_efficiency_report(), content_type="text/html")

@csrf_exempt
def variety_performance_report(request):
    """Отчет производительности сортов для менеджмента"""
    return HttpResponse(get_variety_performance_report(), content_type="text/html")

