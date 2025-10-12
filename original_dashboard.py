"""
Оригинальный дизайн дашборда KFP Reporting
"""
from django.http import HttpResponse

def get_original_dashboard():
    """Возвращает оригинальный дизайн дашборда"""
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
                        <a href="/" class="text-blue-600 hover:text-blue-800 px-3 py-2 rounded font-medium">Дашборд</a>
                        <a href="/upload/" class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded">Загрузка</a>
                        <a href="/reports/" class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded">Отчеты</a>
                        <a href="/admin/" class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded">Admin</a>
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
                <div class="relative bg-white pt-5 px-4 pb-12 sm:pt-6 sm:px-6 shadow rounded-lg overflow-hidden cursor-pointer hover:shadow-md transition-shadow" onclick="window.location.href='/upload/'">
                    <dt>
                        <div class="absolute bg-blue-500 rounded-md p-3">
                            <svg class="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                            </svg>
                        </div>
                        <p class="ml-16 text-sm font-medium text-gray-500 truncate">Всего записей</p>
                    </dt>
                    <dd class="ml-16 pb-6 flex items-baseline sm:pb-7">
                        <p class="text-2xl font-semibold text-gray-900" id="total-records">Загрузка...</p>
                    </dd>
                </div>

                <div class="relative bg-white pt-5 px-4 pb-12 sm:pt-6 sm:px-6 shadow rounded-lg overflow-hidden cursor-pointer hover:shadow-md transition-shadow" onclick="window.location.href='/reports/'">
                    <dt>
                        <div class="absolute bg-green-500 rounded-md p-3">
                            <svg class="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
                            </svg>
                        </div>
                        <p class="ml-16 text-sm font-medium text-gray-500 truncate">Количество полей</p>
                    </dt>
                    <dd class="ml-16 pb-6 flex items-baseline sm:pb-7">
                        <p class="text-2xl font-semibold text-gray-900" id="unique-fields">Загрузка...</p>
                    </dd>
                </div>

                <div class="relative bg-white pt-5 px-4 pb-12 sm:pt-6 sm:px-6 shadow rounded-lg overflow-hidden cursor-pointer hover:shadow-md transition-shadow" onclick="window.location.href='/reports/'">
                    <dt>
                        <div class="absolute bg-yellow-500 rounded-md p-3">
                            <svg class="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path>
                            </svg>
                        </div>
                        <p class="ml-16 text-sm font-medium text-gray-500 truncate">Конечные продукты</p>
                    </dt>
                    <dd class="ml-16 pb-6 flex items-baseline sm:pb-7">
                        <p class="text-2xl font-semibold text-gray-900" id="unique-products">Загрузка...</p>
                    </dd>
                </div>

                <div class="relative bg-white pt-5 px-4 pb-12 sm:pt-6 sm:px-6 shadow rounded-lg overflow-hidden cursor-pointer hover:shadow-md transition-shadow" onclick="window.location.href='/reports/'">
                    <dt>
                        <div class="absolute bg-purple-500 rounded-md p-3">
                            <svg class="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                            </svg>
                        </div>
                        <p class="ml-16 text-sm font-medium text-gray-500 truncate">Сорта</p>
                    </dt>
                    <dd class="ml-16 pb-6 flex items-baseline sm:pb-7">
                        <p class="text-2xl font-semibold text-gray-900" id="unique-varieties">Загрузка...</p>
                    </dd>
                </div>
            </div>

            <!-- Additional Info -->
            <div class="bg-white shadow rounded-lg p-6 mb-8" id="additional-info" style="display: none;">
                <h3 class="text-lg font-medium text-gray-900 mb-4">Дополнительная информация</h3>
                <div class="grid grid-cols-1 gap-4 sm:grid-cols-3">
                    <div class="flex items-center">
                        <svg class="h-5 w-5 text-gray-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                        </svg>
                        <span class="text-sm text-gray-500">Последний год данных:</span>
                        <span class="ml-2 text-sm font-medium text-gray-900" id="latest-year">Нет данных</span>
                    </div>
                    <div class="flex items-center">
                        <svg class="h-5 w-5 text-gray-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path>
                        </svg>
                        <span class="text-sm text-gray-500">Средняя урожайность:</span>
                        <span class="ml-2 text-sm font-medium text-gray-900" id="avg-yield">0 ц/га</span>
                    </div>
                    <div class="flex items-center">
                        <svg class="h-5 w-5 text-gray-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
                        </svg>
                        <span class="text-sm text-gray-500">Общая площадь:</span>
                        <span class="ml-2 text-sm font-medium text-gray-900" id="total-area">0 га</span>
                    </div>
                </div>
            </div>

            <!-- Quick Actions -->
            <div class="bg-white shadow rounded-lg p-6">
                <h3 class="text-lg font-medium text-gray-900 mb-4">Быстрые действия</h3>
                <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
                    <div class="relative group bg-white p-6 focus-within:ring-2 focus-within:ring-inset focus-within:ring-blue-500 rounded-lg border border-gray-200 hover:border-gray-300 cursor-pointer transition-colors" onclick="window.location.href='/upload/'">
                        <div>
                            <span class="bg-blue-500 rounded-lg inline-flex p-3 ring-4 ring-white">
                                <svg class="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
                                </svg>
                            </span>
                        </div>
                        <div class="mt-8">
                            <h3 class="text-lg font-medium">
                                <span class="absolute inset-0" />
                                Загрузить файл
                            </h3>
                            <p class="mt-2 text-sm text-gray-500">
                                Загрузить новые данные CSV/XLSX
                            </p>
                        </div>
                    </div>

                    <div class="relative group bg-white p-6 focus-within:ring-2 focus-within:ring-inset focus-within:ring-green-500 rounded-lg border border-gray-200 hover:border-gray-300 cursor-pointer transition-colors" onclick="window.location.href='/reports/yield-comparison/'">
                        <div>
                            <span class="bg-green-500 rounded-lg inline-flex p-3 ring-4 ring-white">
                                <svg class="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
                                </svg>
                            </span>
                        </div>
                        <div class="mt-8">
                            <h3 class="text-lg font-medium">
                                <span class="absolute inset-0" />
                                Сравнительный отчет
                            </h3>
                            <p class="mt-2 text-sm text-gray-500">
                                Сравнить урожайность по различным параметрам
                            </p>
                        </div>
                    </div>

                    <div class="relative group bg-white p-6 focus-within:ring-2 focus-within:ring-inset focus-within:ring-blue-500 rounded-lg border border-gray-200 hover:border-gray-300 cursor-pointer transition-colors" onclick="window.location.href='/reports/'">
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
                                <span class="absolute inset-0" />
                                Эффективность полей
                            </h3>
                            <p class="mt-2 text-sm text-gray-500">
                                Анализ производительности полей
                            </p>
                        </div>
                    </div>

                    <div class="relative group bg-white p-6 focus-within:ring-2 focus-within:ring-inset focus-within:ring-purple-500 rounded-lg border border-gray-200 hover:border-gray-300 cursor-pointer transition-colors" onclick="window.location.href='/reports/'">
                        <div>
                            <span class="bg-purple-500 rounded-lg inline-flex p-3 ring-4 ring-white">
                                <svg class="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path>
                                </svg>
                            </span>
                        </div>
                        <div class="mt-8">
                            <h3 class="text-lg font-medium">
                                <span class="absolute inset-0" />
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
            // Загружаем статистику дашборда
            async function loadDashboardStats() {
                try {
                    const response = await fetch('/api/reports/dashboard-stats/');
                    if (response.ok) {
                        const data = await response.json();
                        document.getElementById('total-records').textContent = data.total_records || 0;
                        document.getElementById('unique-fields').textContent = data.unique_fields || 0;
                        document.getElementById('unique-products').textContent = data.unique_products || 0;
                        document.getElementById('unique-varieties').textContent = data.unique_varieties || 0;
                        
                        // Показываем дополнительную информацию если есть данные
                        if (data.total_records > 0) {
                            document.getElementById('additional-info').style.display = 'block';
                            document.getElementById('latest-year').textContent = data.latest_year || 'Нет данных';
                            document.getElementById('avg-yield').textContent = (data.avg_yield || 0).toFixed(1) + ' ц/га';
                            document.getElementById('total-area').textContent = (data.total_area || 0).toFixed(1) + ' га';
                        }
                    }
                } catch (error) {
                    console.error('Ошибка загрузки статистики:', error);
                }
            }

            // Загружаем статистику при загрузке страницы
            loadDashboardStats();
        </script>
    </body>
    </html>
    """
