"""
Отчет сравнения урожайности для менеджмента
"""
from django.http import HttpResponse

def get_management_yield_comparison_report():
    """Возвращает отчет сравнения урожайности для менеджмента"""
    return """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>KFP Reporting - Сравнение урожайности</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            /* Prevent table from stretching the page */
            body {
                overflow-x: hidden;
            }
            
            /* Chart container constraints - FORCE STATIC SIZES */
            .chart-container {
                position: relative !important;
                width: 100% !important;
                height: 400px !important;
                max-width: 100% !important;
                max-height: 400px !important;
                min-width: 100% !important;
                min-height: 400px !important;
                overflow: hidden !important;
                margin: 0 auto;
                box-sizing: border-box !important;
            }
            
            /* Canvas constraints - ABSOLUTE STATIC SIZES */
            canvas {
                width: 100% !important;
                height: 400px !important;
                max-width: 100% !important;
                max-height: 400px !important;
                min-width: 100% !important;
                min-height: 400px !important;
                display: block !important;
                position: relative !important;
                transform: none !important;
                scale: 1 !important;
                box-sizing: border-box !important;
                flex-shrink: 0 !important;
                flex-grow: 0 !important;
            }
            
            /* ABSOLUTE PREVENTION of any size changes */
            canvas:hover, canvas:focus, canvas:active, canvas:visited {
                transform: none !important;
                scale: 1 !important;
                width: 100% !important;
                height: 400px !important;
                max-width: 100% !important;
                max-height: 400px !important;
                min-width: 100% !important;
                min-height: 400px !important;
                box-sizing: border-box !important;
                flex-shrink: 0 !important;
                flex-grow: 0 !important;
            }
            
            /* Allow tooltip interactions but prevent stretching */
            .chart-container {
                pointer-events: auto !important;
            }
            
            canvas {
                pointer-events: auto !important;
                user-select: none !important;
                -webkit-user-select: none !important;
                -moz-user-select: none !important;
                -ms-user-select: none !important;
            }
            
            .max-w-7xl {
                max-width: 80rem;
            }
            
            /* Force table to stay within container */
            table {
                table-layout: fixed;
                width: 100%;
            }
            
            /* Ensure text truncation works */
            .truncate {
                overflow: hidden;
                text-overflow: ellipsis;
                white-space: nowrap;
            }
            
            /* Ensure charts don't overflow */
            canvas {
                max-width: 100% !important;
                height: auto !important;
            }
        </style>
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
                        <a href="/" class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded">Дашборд</a>
                        <a href="/upload/" class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded">Загрузка</a>
                        <a href="/reports/" class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded">Отчеты</a>
                        <a href="/reports/yield-comparison/" class="text-blue-600 hover:text-blue-800 px-3 py-2 rounded font-medium">Сравнение урожайности</a>
                        <a href="/admin/" class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded">Admin</a>
                    </div>
                </div>
            </div>
        </nav>

        <!-- Main Content -->
        <div class="max-w-7xl mx-auto px-4 py-8">
            <div class="mb-8">
                <h1 class="text-2xl font-bold text-gray-900">Сравнение урожайности</h1>
                <p class="mt-1 text-sm text-gray-500">
                    Анализ урожайности по сортам и конечным продуктам в разрезе годов и полей
                </p>
            </div>

            <!-- Filters -->
            <div class="bg-white shadow rounded-lg p-6 mb-8">
                <h3 class="text-lg font-medium text-gray-900 mb-4">Фильтры</h3>
                <div class="grid grid-cols-1 gap-4 md:grid-cols-5">
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Год от</label>
                        <select id="year-from-filter" class="w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
                            <option value="">Все годы</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Год до</label>
                        <select id="year-to-filter" class="w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
                            <option value="">Все годы</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Конечный продукт</label>
                        <select id="product-filter" class="w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
                            <option value="">Все продукты</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Поле</label>
                        <select id="field-filter" class="w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
                            <option value="">Все поля</option>
                        </select>
                    </div>
                    <div class="flex items-end">
                        <button onclick="loadReport()" class="w-full bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors">
                            <svg class="w-4 h-4 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
                            </svg>
                            Обновить отчет
                        </button>
                    </div>
                </div>
            </div>

            <!-- Loading State -->
            <div id="loading-state" class="hidden">
                <div class="bg-white shadow rounded-lg p-6 mb-8">
                    <div class="flex items-center justify-center">
                        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mr-3"></div>
                        <span class="text-gray-600">Загрузка данных...</span>
                    </div>
                </div>
            </div>

            <!-- Error State -->
            <div id="error-state" class="hidden">
                <div class="bg-red-50 border border-red-200 rounded-lg p-6 mb-8">
                    <div class="flex items-center">
                        <svg class="h-5 w-5 text-red-400 mr-2" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
                        </svg>
                        <span class="text-red-800 font-medium">Ошибка загрузки данных</span>
                    </div>
                    <p id="error-message" class="text-red-700 text-sm mt-1"></p>
                </div>
            </div>

            <!-- Charts -->
            <div id="charts-container" class="grid grid-cols-1 gap-8 lg:grid-cols-2">
                <!-- Yield by Year -->
                <div class="bg-white shadow rounded-lg p-6">
                    <div class="flex items-center justify-between mb-4">
                        <h3 class="text-lg font-medium text-gray-900">Урожайность по годам</h3>
                        <div class="flex space-x-2">
                            <button onclick="downloadChart('yield-by-year-chart', 'yield-by-year.png')" class="text-gray-400 hover:text-gray-600">
                                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                                </svg>
                            </button>
                        </div>
                    </div>
                <div style="position: relative; width: 100%; height: 400px; max-width: 100%; overflow: hidden;">
                    <canvas id="yield-by-year-chart" width="800" height="400" style="width: 100% !important; height: 400px !important; max-width: 100% !important; max-height: 400px !important; display: block !important;"></canvas>
                </div>
                </div>

                <!-- Yield by Product -->
                <div class="bg-white shadow rounded-lg p-6">
                    <div class="flex items-center justify-between mb-4">
                        <h3 class="text-lg font-medium text-gray-900">Урожайность по продуктам</h3>
                        <div class="flex space-x-2">
                            <button onclick="downloadChart('yield-by-product-chart', 'yield-by-product.png')" class="text-gray-400 hover:text-gray-600">
                                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                                </svg>
                            </button>
                        </div>
                    </div>
                <div style="position: relative; width: 100%; height: 400px; max-width: 100%; overflow: hidden;">
                    <canvas id="yield-by-product-chart" width="800" height="400" style="width: 100% !important; height: 400px !important; max-width: 100% !important; max-height: 400px !important; display: block !important;"></canvas>
                </div>
                </div>
            </div>

            <!-- Variety Performance -->
            <div class="mt-8 bg-white shadow rounded-lg p-6">
                <div class="flex items-center justify-between mb-4">
                    <h3 class="text-lg font-medium text-gray-900">Производительность сортов</h3>
                    <div class="flex space-x-2">
                        <button onclick="exportTable('variety-table')" class="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 focus:ring-2 focus:ring-green-500 focus:ring-offset-2 transition-colors">
                            <svg class="w-4 h-4 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                            </svg>
                            Экспорт CSV
                        </button>
                    </div>
                </div>
                <div class="overflow-x-auto">
                    <table id="variety-table" class="min-w-full divide-y divide-gray-200">
                        <thead class="bg-gray-50">
                            <tr>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Сорт</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Конечный продукт</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Средняя урожайность</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Максимальная урожайность</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Количество записей</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Поля</th>
                            </tr>
                        </thead>
                        <tbody id="variety-table-body" class="bg-white divide-y divide-gray-200">
                            <tr>
                                <td colspan="6" class="px-6 py-4 text-center text-gray-500">Загрузите данные для отображения таблицы</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Field Performance -->
            <div class="mt-8 bg-white shadow rounded-lg p-6">
                <div class="flex items-center justify-between mb-4">
                    <h3 class="text-lg font-medium text-gray-900">Производительность полей</h3>
                    <div class="flex space-x-2">
                        <button onclick="exportTable('field-table')" class="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 focus:ring-2 focus:ring-green-500 focus:ring-offset-2 transition-colors">
                            <svg class="w-4 h-4 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                            </svg>
                            Экспорт CSV
                        </button>
                    </div>
                </div>
                <div class="overflow-x-auto">
                    <table id="field-table" class="min-w-full divide-y divide-gray-200">
                        <thead class="bg-gray-50">
                            <tr>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Поле</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Средняя урожайность</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Общая площадь</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Количество продуктов</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Годы данных</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Количество записей</th>
                            </tr>
                        </thead>
                        <tbody id="field-table-body" class="bg-white divide-y divide-gray-200">
                            <tr>
                                <td colspan="6" class="px-6 py-4 text-center text-gray-500">Загрузите данные для отображения таблицы</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <script>
            let yieldByYearChart, yieldByProductChart;

            async function loadReport() {
                const loadingState = document.getElementById('loading-state');
                const chartsContainer = document.getElementById('charts-container');
                const errorState = document.getElementById('error-state');
                
                loadingState.classList.remove('hidden');
                chartsContainer.classList.add('hidden');
                errorState.classList.add('hidden');

                try {
                    const yearFrom = document.getElementById('year-from-filter').value;
                    const yearTo = document.getElementById('year-to-filter').value;
                    const product = document.getElementById('product-filter').value;
                    const field = document.getElementById('field-filter').value;

                    const params = new URLSearchParams();
                    if (yearFrom) params.append('year_from', yearFrom);
                    if (yearTo) params.append('year_to', yearTo);
                    if (product) params.append('final_product', product);
                    if (field) params.append('field_name', field);

                    const response = await fetch(`/api/reports/yield-comparison/?${params}`);
                    
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    
                    const data = await response.json();
                    console.log('Received data:', data);

                    updateCharts(data); // ENABLED - STATIC SVG CHARTS
                    updateVarietyTable(data);
                    updateFieldTable(data);
                    updateFilters(data);

                } catch (error) {
                    console.error('Error loading report:', error);
                    errorState.classList.remove('hidden');
                    document.getElementById('error-message').textContent = error.message;
                } finally {
                    loadingState.classList.add('hidden');
                    chartsContainer.classList.remove('hidden');
                }
            }

            function updateCharts(data) {
                // Yield by Year Chart with strict size limits
                const yearCtx = document.getElementById('yield-by-year-chart').getContext('2d');
                if (yieldByYearChart) yieldByYearChart.destroy();
                
                yieldByYearChart = new Chart(yearCtx, {
                    type: 'line',
                    data: {
                        labels: data.years || [],
                        datasets: [{
                            label: 'Урожайность (ц/га)',
                            data: data.yield_by_year || [],
                            borderColor: 'rgb(34, 197, 94)',
                            backgroundColor: 'rgba(34, 197, 94, 0.1)',
                            tension: 0.4,
                            fill: true,
                            pointBackgroundColor: 'rgb(34, 197, 94)',
                            pointBorderColor: '#fff',
                            pointBorderWidth: 2,
                            pointRadius: 6
                        }]
                    },
                    options: {
                        responsive: false,
                        maintainAspectRatio: false,
                        devicePixelRatio: 1,
                        resizeDelay: 0,
                        plugins: {
                            legend: {
                                display: true,
                                position: 'top'
                            },
                            tooltip: {
                                enabled: true,
                                mode: 'index',
                                intersect: false,
                                backgroundColor: 'rgba(0, 0, 0, 0.8)',
                                titleColor: 'white',
                                bodyColor: 'white',
                                borderColor: 'rgba(255, 255, 255, 0.2)',
                                borderWidth: 1
                            }
                        },
                        scales: {
                            y: {
                                beginAtZero: true,
                                title: {
                                    display: true,
                                    text: 'Урожайность (ц/га)'
                                }
                            }
                        },
                        animation: {
                            duration: 0
                        },
                        interaction: {
                            intersect: false,
                            mode: 'index'
                        },
                        onHover: function(event, elements) {
                            // Allow tooltips but prevent stretching
                            event.target.style.cursor = 'pointer';
                        },
                        onClick: function(event, elements) {
                            // Allow clicks for tooltips
                            return true;
                        }
                    }
                });
                
                // Force dimensions after chart creation
                setTimeout(forceStaticChartDimensions, 50);

                // Yield by Product Chart with strict size limits
                const productCtx = document.getElementById('yield-by-product-chart').getContext('2d');
                if (yieldByProductChart) yieldByProductChart.destroy();
                
                yieldByProductChart = new Chart(productCtx, {
                    type: 'bar',
                    data: {
                        labels: data.products || [],
                        datasets: [{
                            label: 'Урожайность (ц/га)',
                            data: data.yield_by_product || [],
                            backgroundColor: [
                                'rgba(59, 130, 246, 0.8)',
                                'rgba(34, 197, 94, 0.8)',
                                'rgba(251, 191, 36, 0.8)',
                                'rgba(239, 68, 68, 0.8)',
                                'rgba(147, 51, 234, 0.8)',
                                'rgba(236, 72, 153, 0.8)',
                                'rgba(6, 182, 212, 0.8)'
                            ],
                            borderColor: [
                                'rgba(59, 130, 246, 1)',
                                'rgba(34, 197, 94, 1)',
                                'rgba(251, 191, 36, 1)',
                                'rgba(239, 68, 68, 1)',
                                'rgba(147, 51, 234, 1)',
                                'rgba(236, 72, 153, 1)',
                                'rgba(6, 182, 212, 1)'
                            ],
                            borderWidth: 1
                        }]
                    },
                    options: {
                        responsive: false,
                        maintainAspectRatio: false,
                        devicePixelRatio: 1,
                        resizeDelay: 0,
                        plugins: {
                            legend: {
                                display: true,
                                position: 'top'
                            },
                            tooltip: {
                                enabled: true,
                                mode: 'index',
                                intersect: false,
                                backgroundColor: 'rgba(0, 0, 0, 0.8)',
                                titleColor: 'white',
                                bodyColor: 'white',
                                borderColor: 'rgba(255, 255, 255, 0.2)',
                                borderWidth: 1
                            }
                        },
                        scales: {
                            y: {
                                beginAtZero: true,
                                title: {
                                    display: true,
                                    text: 'Урожайность (ц/га)'
                                }
                            }
                        },
                        animation: {
                            duration: 0
                        },
                        interaction: {
                            intersect: false,
                            mode: 'index'
                        },
                        onHover: function(event, elements) {
                            // Allow tooltips but prevent stretching
                            event.target.style.cursor = 'pointer';
                        },
                        onClick: function(event, elements) {
                            // Allow clicks for tooltips
                            return true;
                        }
                    }
                });
                
                // Force dimensions after chart creation
                setTimeout(forceStaticChartDimensions, 50);
            }

            function updateVarietyTable(data) {
                const tbody = document.getElementById('variety-table-body');
                tbody.innerHTML = '';

                if (data.variety_comparison && data.variety_comparison.length > 0) {
                    data.variety_comparison.forEach(row => {
                        const tr = document.createElement('tr');
                        tr.className = 'hover:bg-gray-50';
                        tr.innerHTML = `
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${row.variety || '-'}</td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${row.final_product || '-'}</td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${row.avg_yield?.toFixed(2) || '0.00'} ц/га</td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${row.max_yield?.toFixed(2) || '0.00'} ц/га</td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${row.count || 0}</td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${row.fields || '-'}</td>
                        `;
                        tbody.appendChild(tr);
                    });
                } else {
                    tbody.innerHTML = '<tr><td colspan="6" class="px-6 py-4 text-center text-gray-500">Нет данных для отображения</td></tr>';
                }
            }

            function updateFieldTable(data) {
                const tbody = document.getElementById('field-table-body');
                tbody.innerHTML = '';

                if (data.field_comparison && data.field_comparison.length > 0) {
                    data.field_comparison.forEach(row => {
                        const tr = document.createElement('tr');
                        tr.className = 'hover:bg-gray-50';
                        tr.innerHTML = `
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${row.field_name || '-'}</td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${row.avg_yield?.toFixed(2) || '0.00'} ц/га</td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${row.total_area?.toFixed(2) || '0.00'} га</td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${row.product_count || 0}</td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${row.year_count || 0}</td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${row.record_count || 0}</td>
                        `;
                        tbody.appendChild(tr);
                    });
                } else {
                    tbody.innerHTML = '<tr><td colspan="6" class="px-6 py-4 text-center text-gray-500">Нет данных для отображения</td></tr>';
                }
            }

            function updateFilters(data) {
                // Update year filters
                const yearFromSelect = document.getElementById('year-from-filter');
                const yearToSelect = document.getElementById('year-to-filter');
                const currentYearFrom = yearFromSelect.value;
                const currentYearTo = yearToSelect.value;
                
                yearFromSelect.innerHTML = '<option value="">Все годы</option>';
                yearToSelect.innerHTML = '<option value="">Все годы</option>';
                
                if (data.years) {
                    const uniqueYears = [...new Set(data.years)].sort();
                    uniqueYears.forEach(year => {
                        const optionFrom = document.createElement('option');
                        optionFrom.value = year;
                        optionFrom.textContent = year;
                        if (year == currentYearFrom) optionFrom.selected = true;
                        yearFromSelect.appendChild(optionFrom);

                        const optionTo = document.createElement('option');
                        optionTo.value = year;
                        optionTo.textContent = year;
                        if (year == currentYearTo) optionTo.selected = true;
                        yearToSelect.appendChild(optionTo);
                    });
                }

                // Update product filter
                const productSelect = document.getElementById('product-filter');
                const currentProduct = productSelect.value;
                productSelect.innerHTML = '<option value="">Все продукты</option>';
                
                if (data.products) {
                    data.products.forEach(product => {
                        const option = document.createElement('option');
                        option.value = product;
                        option.textContent = product;
                        if (product == currentProduct) option.selected = true;
                        productSelect.appendChild(option);
                    });
                }
            }

            function downloadChart(chartId, filename) {
                const canvas = document.getElementById(chartId);
                const url = canvas.toDataURL('image/png');
                const link = document.createElement('a');
                link.download = filename;
                link.href = url;
                link.click();
            }

            function exportTable(tableId) {
                const table = document.getElementById(tableId);
                let csv = '';
                
                // Get headers
                const headers = [];
                table.querySelectorAll('thead th').forEach(th => {
                    headers.push(th.textContent.trim());
                });
                csv += headers.join(',') + '\\n';
                
                // Get rows
                table.querySelectorAll('tbody tr').forEach(row => {
                    const cells = row.querySelectorAll('td');
                    if (cells.length > 0) {
                        const rowData = Array.from(cells).map(cell => cell.textContent.trim()).join(',');
                        csv += rowData + '\\n';
                    }
                });
                
                const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
                const link = document.createElement('a');
                link.href = URL.createObjectURL(blob);
                link.download = tableId + '-report.csv';
                link.click();
            }

            // Force chart dimensions to be static
            function forceStaticChartDimensions() {
                const yearChart = document.getElementById('yield-by-year-chart');
                const productChart = document.getElementById('yield-by-product-chart');
                
                if (yearChart) {
                    yearChart.style.width = '100%';
                    yearChart.style.height = '400px';
                    yearChart.style.maxWidth = '100%';
                    yearChart.style.maxHeight = '400px';
                    yearChart.style.minWidth = '100%';
                    yearChart.style.minHeight = '400px';
                }
                
                if (productChart) {
                    productChart.style.width = '100%';
                    productChart.style.height = '400px';
                    productChart.style.maxWidth = '100%';
                    productChart.style.maxHeight = '400px';
                    productChart.style.minWidth = '100%';
                    productChart.style.minHeight = '400px';
                }
            }
            
            // Monitor and force dimensions continuously
            function startDimensionMonitoring() {
                setInterval(forceStaticChartDimensions, 100);
                
                // Force dimensions on any resize
                window.addEventListener('resize', forceStaticChartDimensions);
                
                // Force dimensions on any scroll
                window.addEventListener('scroll', forceStaticChartDimensions);
                
                // Force dimensions on any mouse move
                document.addEventListener('mousemove', forceStaticChartDimensions);
            }

            // Load data on page load
            document.addEventListener('DOMContentLoaded', function() {
                // Start dimension monitoring
                startDimensionMonitoring();
                
                // Load report data
                loadReport();
            });
        </script>
    </body>
    </html>
    """
