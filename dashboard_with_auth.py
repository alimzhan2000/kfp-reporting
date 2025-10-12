"""
Дашборд с авторизацией для KFP Reporting
"""
from django.http import HttpResponse

def get_dashboard_with_auth():
    """Возвращает дашборд с проверкой авторизации"""
    return """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Reporting KFP</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="https://unpkg.com/lucide@latest/dist/umd/lucide.js"></script>
    </head>
    <body class="bg-gray-50">
        <!-- Header -->
        <nav class="bg-white shadow">
            <div class="max-w-7xl mx-auto px-4">
                <div class="flex justify-between items-center py-4">
                    <div class="flex items-center">
                        <div class="text-2xl mr-3">🌾</div>
                        <h1 class="text-gray-900 text-xl font-bold">Reporting KFP</h1>
                    </div>
                    <div class="flex items-center space-x-4">
                        <a href="/dashboard/" class="text-blue-600 hover:text-blue-800 px-3 py-2 rounded font-medium">Дашборд</a>
                        <a href="/upload/" class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded">Загрузка</a>
                        <a href="/reports/" class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded">Отчеты</a>
                        <a href="/admin/" class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded">Admin</a>
                        <div class="flex items-center space-x-2">
                            <span id="user-info" class="text-sm text-gray-600"></span>
                            <button onclick="logout()" class="text-red-600 hover:text-red-800 px-2 py-1 rounded text-sm">
                                Выйти
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </nav>

        <!-- Main Content -->
        <div class="max-w-7xl mx-auto px-4 py-8">
            <div class="mb-8">
                <h1 class="text-2xl font-bold text-gray-900">Дашборд</h1>
                <p class="mt-1 text-sm text-gray-500">
                    Обзор сельскохозяйственных данных и отчетов
                </p>
            </div>

            <!-- Stats Grid -->
            <div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4 mb-8">
                <!-- Total Records -->
                <div class="relative bg-white pt-5 px-4 pb-12 sm:pt-6 sm:px-6 shadow rounded-lg overflow-hidden">
                    <dt>
                        <div class="absolute bg-blue-500 rounded-md p-3">
                            <i data-lucide="database" class="h-6 w-6 text-white"></i>
                        </div>
                        <p class="ml-16 text-sm font-medium text-gray-500 truncate">Всего записей</p>
                    </dt>
                    <dd class="ml-16 pb-6 flex items-baseline sm:pb-7">
                        <p class="text-2xl font-semibold text-gray-900" id="total-records">Загрузка...</p>
                    </dd>
                </div>

                <!-- Fields Count -->
                <div class="relative bg-white pt-5 px-4 pb-12 sm:pt-6 sm:px-6 shadow rounded-lg overflow-hidden">
                    <dt>
                        <div class="absolute bg-green-500 rounded-md p-3">
                            <i data-lucide="map-pin" class="h-6 w-6 text-white"></i>
                        </div>
                        <p class="ml-16 text-sm font-medium text-gray-500 truncate">Количество полей</p>
                    </dt>
                    <dd class="ml-16 pb-6 flex items-baseline sm:pb-7">
                        <p class="text-2xl font-semibold text-gray-900" id="fields-count">Загрузка...</p>
                    </dd>
                </div>

                <!-- Products Count -->
                <div class="relative bg-white pt-5 px-4 pb-12 sm:pt-6 sm:px-6 shadow rounded-lg overflow-hidden">
                    <dt>
                        <div class="absolute bg-yellow-500 rounded-md p-3">
                            <i data-lucide="package" class="h-6 w-6 text-white"></i>
                        </div>
                        <p class="ml-16 text-sm font-medium text-gray-500 truncate">Конечные продукты</p>
                    </dt>
                    <dd class="ml-16 pb-6 flex items-baseline sm:pb-7">
                        <p class="text-2xl font-semibold text-gray-900" id="products-count">Загрузка...</p>
                    </dd>
                </div>

                <!-- Varieties Count -->
                <div class="relative bg-white pt-5 px-4 pb-12 sm:pt-6 sm:px-6 shadow rounded-lg overflow-hidden">
                    <dt>
                        <div class="absolute bg-purple-500 rounded-md p-3">
                            <i data-lucide="leaf" class="h-6 w-6 text-white"></i>
                        </div>
                        <p class="ml-16 text-sm font-medium text-gray-500 truncate">Сорта</p>
                    </dt>
                    <dd class="ml-16 pb-6 flex items-baseline sm:pb-7">
                        <p class="text-2xl font-semibold text-gray-900" id="varieties-count">Загрузка...</p>
                    </dd>
                </div>
            </div>

            <!-- Additional Info -->
            <div class="bg-white shadow rounded-lg p-6 mb-8">
                <h3 class="text-lg font-medium text-gray-900 mb-4">Дополнительная информация</h3>
                <div class="grid grid-cols-1 gap-4 sm:grid-cols-3">
                    <div>
                        <dt class="text-sm font-medium text-gray-500">Последний год данных</dt>
                        <dd class="mt-1 text-sm text-gray-900" id="last-year">Нет данных</dd>
                    </div>
                    <div>
                        <dt class="text-sm font-medium text-gray-500">Средняя урожайность</dt>
                        <dd class="mt-1 text-sm text-gray-900" id="avg-yield">0 ц/га</dd>
                    </div>
                    <div>
                        <dt class="text-sm font-medium text-gray-500">Общая площадь</dt>
                        <dd class="mt-1 text-sm text-gray-900" id="total-area">0 га</dd>
                    </div>
                </div>
            </div>

            <!-- Quick Actions -->
            <div class="mb-8">
                <h3 class="text-lg font-medium text-gray-900 mb-4">Быстрые действия</h3>
                <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
                    <!-- Upload File -->
                    <div class="relative group bg-white p-6 focus-within:ring-2 focus-within:ring-inset focus-within:ring-blue-500 rounded-lg shadow hover:shadow-md transition-shadow cursor-pointer" onclick="window.location.href='/upload/'">
                        <div>
                            <span class="rounded-lg inline-flex p-3 bg-blue-50 text-blue-700 ring-4 ring-white">
                                <i data-lucide="upload" class="h-6 w-6"></i>
                            </span>
                        </div>
                        <div class="mt-4">
                            <h3 class="text-lg font-medium text-gray-900">
                                Загрузить файл
                            </h3>
                            <p class="mt-2 text-sm text-gray-500">
                                Загрузить новые данные CSV/XLSX
                            </p>
                        </div>
                    </div>

                    <!-- Yield Comparison -->
                    <div class="relative group bg-white p-6 focus-within:ring-2 focus-within:ring-inset focus-within:ring-green-500 rounded-lg shadow hover:shadow-md transition-shadow cursor-pointer" onclick="window.location.href='/reports/yield-comparison/'">
                        <div>
                            <span class="rounded-lg inline-flex p-3 bg-green-50 text-green-700 ring-4 ring-white">
                                <i data-lucide="bar-chart-3" class="h-6 w-6"></i>
                            </span>
                        </div>
                        <div class="mt-4">
                            <h3 class="text-lg font-medium text-gray-900">
                                Сравнительный отчет
                            </h3>
                            <p class="mt-2 text-sm text-gray-500">
                                Сравнить урожайность по различным параметрам
                            </p>
                        </div>
                    </div>

                    <!-- Field Efficiency -->
                    <div class="relative group bg-white p-6 focus-within:ring-2 focus-within:ring-inset focus-within:ring-blue-500 rounded-lg shadow hover:shadow-md transition-shadow cursor-pointer" onclick="window.location.href='/reports/field-efficiency/'">
                        <div>
                            <span class="rounded-lg inline-flex p-3 bg-blue-50 text-blue-700 ring-4 ring-white">
                                <i data-lucide="map-pin" class="h-6 w-6"></i>
                            </span>
                        </div>
                        <div class="mt-4">
                            <h3 class="text-lg font-medium text-gray-900">
                                Эффективность полей
                            </h3>
                            <p class="mt-2 text-sm text-gray-500">
                                Анализ производительности полей
                            </p>
                        </div>
                    </div>

                    <!-- Variety Performance -->
                    <div class="relative group bg-white p-6 focus-within:ring-2 focus-within:ring-inset focus-within:ring-purple-500 rounded-lg shadow hover:shadow-md transition-shadow cursor-pointer" onclick="window.location.href='/reports/variety-performance/'">
                        <div>
                            <span class="rounded-lg inline-flex p-3 bg-purple-50 text-purple-700 ring-4 ring-white">
                                <i data-lucide="trending-up" class="h-6 w-6"></i>
                            </span>
                        </div>
                        <div class="mt-4">
                            <h3 class="text-lg font-medium text-gray-900">
                                Производительность сортов
                            </h3>
                            <p class="mt-2 text-sm text-gray-500">
                                Сравнение сортов в рамках культур
                            </p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Admin Section (only for admin users) -->
            <div id="admin-section" class="hidden bg-white shadow rounded-lg p-6">
                <h3 class="text-lg font-medium text-gray-900 mb-4">Управление пользователями</h3>
                <p class="text-sm text-gray-500 mb-4">Управление доступом к системе и отчетам</p>
                <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
                    <button class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700">
                        Добавить пользователя
                    </button>
                    <button class="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700">
                        Управление доступом
                    </button>
                    <button class="bg-purple-600 text-white px-4 py-2 rounded-md hover:bg-purple-700">
                        Логи системы
                    </button>
                </div>
            </div>
        </div>

        <script>
            // Initialize Lucide icons
            lucide.createIcons();

            // Check authentication
            function checkAuth() {
                const userData = localStorage.getItem('kfp_user');
                if (!userData) {
                    window.location.href = '/login/';
                    return null;
                }
                
                const user = JSON.parse(userData);
                document.getElementById('user-info').textContent = `${user.username} (${user.role})`;
                
                // Show admin section for admin users
                if (user.role === 'admin') {
                    document.getElementById('admin-section').classList.remove('hidden');
                }
                
                return user;
            }

            // Logout function
            function logout() {
                localStorage.removeItem('kfp_user');
                window.location.href = '/login/';
            }

            // Load dashboard stats
            async function loadStats() {
                try {
                    const response = await fetch('/api/reports/dashboard-stats/');
                    if (response.ok) {
                        const data = await response.json();
                        document.getElementById('total-records').textContent = data.total_records || 0;
                        document.getElementById('fields-count').textContent = data.unique_fields || 0;
                        document.getElementById('products-count').textContent = data.unique_products || 0;
                        document.getElementById('varieties-count').textContent = data.unique_varieties || 0;
                        document.getElementById('last-year').textContent = data.last_year || 'Нет данных';
                        document.getElementById('avg-yield').textContent = `${data.avg_yield || 0} ц/га`;
                        document.getElementById('total-area').textContent = `${data.total_area || 0} га`;
                    }
                } catch (error) {
                    console.error('Error loading stats:', error);
                }
            }

            // Initialize dashboard
            const user = checkAuth();
            if (user) {
                loadStats();
            }
        </script>
    </body>
    </html>
    """
