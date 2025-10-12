"""
Оригинальный дизайн отчета сравнения урожайности
"""
from django.http import HttpResponse

def get_original_yield_comparison_report():
    """Возвращает оригинальный дизайн отчета сравнения урожайности"""
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
            /* STATIC DIMENSIONS - NO STRETCHING ALLOWED */
            * {
                box-sizing: border-box !important;
                max-width: 100vw !important;
            }
            
            body {
                overflow-x: hidden !important;
                max-width: 100vw !important;
                margin: 0 !important;
                padding: 0 !important;
                width: 100vw !important;
            }
            
            .max-w-7xl {
                max-width: 80rem !important;
                width: 100% !important;
                overflow-x: hidden !important;
            }
            
            /* STATIC CHART CONTAINERS - FIXED DIMENSIONS */
            .bg-white.shadow.rounded-lg.p-6 {
                overflow: hidden !important;
                position: relative !important;
                max-width: 100% !important;
                width: 100% !important;
                height: 450px !important; /* Fixed height */
                box-sizing: border-box !important;
            }
            
            /* STATIC CHART CONTAINER - NO EXPANSION */
            #charts-container {
                max-width: 100% !important;
                overflow: hidden !important;
                width: 100% !important;
                height: 450px !important; /* Fixed height */
                box-sizing: border-box !important;
                display: grid !important;
                grid-template-columns: 1fr 1fr !important;
                gap: 2rem !important;
            }
            
            /* STATIC CHART WRAPPERS - ABSOLUTE POSITIONING */
            .chart-wrapper {
                max-width: 100% !important;
                overflow: hidden !important;
                position: relative !important;
                width: 100% !important;
                height: 400px !important; /* Fixed height */
                box-sizing: border-box !important;
            }
            
            /* STATIC CANVAS - ABSOLUTE DIMENSIONS */
            canvas {
                max-width: 100% !important;
                max-height: 350px !important;
                width: 100% !important;
                height: 350px !important; /* Fixed height */
                display: block !important;
                box-sizing: border-box !important;
                position: absolute !important;
                top: 50px !important;
                left: 0 !important;
                right: 0 !important;
            }
            
            /* STATIC CHART SPECIFIC - NO CHANGES ALLOWED */
            #yield-by-year-chart, #yield-by-product-chart {
                max-width: 100% !important;
                max-height: 350px !important;
                width: 100% !important;
                height: 350px !important; /* Fixed height */
                display: block !important;
                box-sizing: border-box !important;
                position: absolute !important;
                top: 50px !important;
                left: 0 !important;
                right: 0 !important;
            }
            
            /* STATIC GRID - NO EXPANSION */
            .grid.grid-cols-1.gap-8.lg\\:grid-cols-2 {
                max-width: 100% !important;
                width: 100% !important;
                height: 450px !important; /* Fixed height */
                overflow: hidden !important;
                box-sizing: border-box !important;
                display: grid !important;
                grid-template-columns: 1fr 1fr !important;
                gap: 2rem !important;
            }
            
            /* STATIC TOOLTIP - NO OVERFLOW - COMPLETELY FIXED */
            .chartjs-tooltip {
                max-width: 200px !important;
                word-wrap: break-word !important;
                overflow-wrap: break-word !important;
                box-sizing: border-box !important;
                position: fixed !important;
                z-index: 1000 !important;
                left: 50% !important;
                top: 50% !important;
                transform: translate(-50%, -50%) !important;
                pointer-events: none !important;
            }
            
            /* PREVENT ALL CHART.JS INTERACTIONS */
            canvas {
                pointer-events: none !important;
                touch-action: none !important;
                user-select: none !important;
                -webkit-user-select: none !important;
                -moz-user-select: none !important;
                -ms-user-select: none !important;
            }
            
            /* LOCK ALL CHART CONTAINERS */
            .chart-wrapper {
                pointer-events: none !important;
                touch-action: none !important;
                user-select: none !important;
            }
            
            /* PREVENT HOVER EFFECTS */
            canvas:hover, .chart-wrapper:hover {
                transform: none !important;
                scale: 1 !important;
                width: 100% !important;
                height: 350px !important;
                max-width: 100% !important;
                max-height: 350px !important;
            }
            
            /* PREVENT ALL HORIZONTAL SCROLL */
            html, body {
                overflow-x: hidden !important;
                max-width: 100vw !important;
            }
            
            /* STATIC RESPONSIVE BEHAVIOR */
            @media (max-width: 768px) {
                #charts-container {
                    grid-template-columns: 1fr !important;
                    height: 900px !important; /* Double height for mobile */
                }
                
                .chart-wrapper {
                    height: 400px !important;
                }
                
                canvas, #yield-by-year-chart, #yield-by-product-chart {
                    height: 350px !important;
                }
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
                        <a href="/dashboard/" class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded">Дашборд</a>
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
                    Анализ урожайности по различным параметрам
                </p>
            </div>

            <!-- Filters -->
            <div class="bg-white shadow rounded-lg p-6 mb-8">
                <h3 class="text-lg font-medium text-gray-900 mb-4">Фильтры</h3>
                <div class="grid grid-cols-1 gap-4 md:grid-cols-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Год</label>
                        <select id="year-filter" class="w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
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

            <!-- Charts -->
            <div id="charts-container" class="grid grid-cols-1 gap-8 lg:grid-cols-2">
                <!-- Yield by Year -->
                <div class="bg-white shadow rounded-lg p-6 chart-wrapper">
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
                    <canvas id="yield-by-year-chart" width="400" height="300"></canvas>
                </div>

                <!-- Yield by Product -->
                <div class="bg-white shadow rounded-lg p-6 chart-wrapper">
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
                    <canvas id="yield-by-product-chart" width="400" height="300"></canvas>
                </div>
            </div>

            <!-- Summary Table -->
            <div class="mt-8 bg-white shadow rounded-lg p-6">
                <div class="flex items-center justify-between mb-4">
                    <h3 class="text-lg font-medium text-gray-900">Сводная таблица</h3>
                    <div class="flex space-x-2">
                        <button onclick="exportTable()" class="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 focus:ring-2 focus:ring-green-500 focus:ring-offset-2 transition-colors">
                            <svg class="w-4 h-4 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                            </svg>
                            Экспорт CSV
                        </button>
                    </div>
                </div>
                <div class="overflow-x-auto">
                    <table class="min-w-full divide-y divide-gray-200">
                        <thead class="bg-gray-50">
                            <tr>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Год</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Конечный продукт</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Средняя урожайность</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Максимальная урожайность</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Количество записей</th>
                            </tr>
                        </thead>
                        <tbody id="summary-table-body" class="bg-white divide-y divide-gray-200">
                            <tr>
                                <td colspan="5" class="px-6 py-4 text-center text-gray-500">Загрузите данные для отображения таблицы</td>
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
                
                loadingState.classList.remove('hidden');
                chartsContainer.classList.add('hidden');

                try {
                    const year = document.getElementById('year-filter').value;
                    const product = document.getElementById('product-filter').value;
                    const field = document.getElementById('field-filter').value;

                    const params = new URLSearchParams();
                    if (year) params.append('year_from', year);
                    if (year) params.append('year_to', year);
                    if (product) params.append('final_product', product);
                    if (field) params.append('field_name', field);

                    const response = await fetch(`/api/reports/yield-comparison/?${params}`);
                    
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    
                    const data = await response.json();

                    updateCharts(data);
                    updateTable(data);
                    updateFilters(data);

                } catch (error) {
                    console.error('Error loading report:', error);
                    alert('Ошибка загрузки данных: ' + error.message);
                } finally {
                    loadingState.classList.add('hidden');
                    chartsContainer.classList.remove('hidden');
                }
            }

            function updateCharts(data) {
                // STATIC DIMENSIONS - NO CALCULATIONS
                const STATIC_WIDTH = 400;  // Fixed width
                const STATIC_HEIGHT = 300; // Fixed height

                // Yield by Year Chart
                const yearCtx = document.getElementById('yield-by-year-chart').getContext('2d');
                if (yieldByYearChart) yieldByYearChart.destroy();
                
                // Set STATIC canvas dimensions
                const yearCanvas = document.getElementById('yield-by-year-chart');
                yearCanvas.width = STATIC_WIDTH;
                yearCanvas.height = STATIC_HEIGHT;
                yearCanvas.style.width = STATIC_WIDTH + 'px';
                yearCanvas.style.height = STATIC_HEIGHT + 'px';
                yearCanvas.style.maxWidth = STATIC_WIDTH + 'px';
                yearCanvas.style.maxHeight = STATIC_HEIGHT + 'px';
                yearCanvas.style.display = 'block';
                yearCanvas.style.position = 'absolute';
                yearCanvas.style.top = '50px';
                yearCanvas.style.left = '0';
                yearCanvas.style.right = '0';
                
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
                            pointRadius: 4 // Smaller points for static chart
                        }]
                    },
                    options: {
                        responsive: false, // STATIC - NO RESPONSIVE
                        maintainAspectRatio: false, // STATIC - NO ASPECT RATIO
                        animation: false, // NO ANIMATIONS TO PREVENT STRETCHING
                        interaction: {
                            intersect: false,
                            mode: 'nearest',
                            axis: 'xy'
                        },
                        onHover: function(event, elements) {
                            // Prevent any hover interactions
                            event.stopPropagation();
                            return false;
                        },
                        onClick: function(event, elements) {
                            // Prevent any click interactions
                            event.stopPropagation();
                            return false;
                        },
                        scales: {
                            y: {
                                beginAtZero: true,
                                title: {
                                    display: true,
                                    text: 'Урожайность (ц/га)',
                                    font: { size: 10 } // Smaller font
                                },
                                ticks: { font: { size: 9 } } // Smaller ticks
                            },
                            x: {
                                ticks: { font: { size: 9 } } // Smaller ticks
                            }
                        },
                        plugins: {
                            legend: {
                                display: true,
                                position: 'top',
                                labels: { font: { size: 10 } } // Smaller legend
                            },
                            tooltip: {
                                enabled: false // COMPLETELY DISABLE TOOLTIPS
                            }
                        }
                    }
                });

                // Yield by Product Chart
                const productCtx = document.getElementById('yield-by-product-chart').getContext('2d');
                if (yieldByProductChart) yieldByProductChart.destroy();
                
                // Set STATIC canvas dimensions
                const productCanvas = document.getElementById('yield-by-product-chart');
                productCanvas.width = STATIC_WIDTH;
                productCanvas.height = STATIC_HEIGHT;
                productCanvas.style.width = STATIC_WIDTH + 'px';
                productCanvas.style.height = STATIC_HEIGHT + 'px';
                productCanvas.style.maxWidth = STATIC_WIDTH + 'px';
                productCanvas.style.maxHeight = STATIC_HEIGHT + 'px';
                productCanvas.style.display = 'block';
                productCanvas.style.position = 'absolute';
                productCanvas.style.top = '50px';
                productCanvas.style.left = '0';
                productCanvas.style.right = '0';
                
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
                        responsive: false, // STATIC - NO RESPONSIVE
                        maintainAspectRatio: false, // STATIC - NO ASPECT RATIO
                        animation: false, // NO ANIMATIONS TO PREVENT STRETCHING
                        interaction: {
                            intersect: false,
                            mode: 'nearest',
                            axis: 'xy'
                        },
                        onHover: function(event, elements) {
                            // Prevent any hover interactions
                            event.stopPropagation();
                            return false;
                        },
                        onClick: function(event, elements) {
                            // Prevent any click interactions
                            event.stopPropagation();
                            return false;
                        },
                        scales: {
                            y: {
                                beginAtZero: true,
                                title: {
                                    display: true,
                                    text: 'Урожайность (ц/га)',
                                    font: { size: 10 } // Smaller font
                                },
                                ticks: { font: { size: 9 } } // Smaller ticks
                            },
                            x: {
                                ticks: { font: { size: 9 } } // Smaller ticks
                            }
                        },
                        plugins: {
                            legend: {
                                display: true,
                                position: 'top',
                                labels: { font: { size: 10 } } // Smaller legend
                            },
                            tooltip: {
                                enabled: false // COMPLETELY DISABLE TOOLTIPS
                            }
                        }
                    }
                });
                
                // COMPLETELY DISABLE ALL INTERACTIONS AFTER CHART CREATION
                setTimeout(() => {
                    // Disable all mouse events on canvas
                    yearCanvas.style.pointerEvents = 'none';
                    yearCanvas.style.touchAction = 'none';
                    yearCanvas.style.userSelect = 'none';
                    yearCanvas.style.webkitUserSelect = 'none';
                    yearCanvas.style.mozUserSelect = 'none';
                    yearCanvas.style.msUserSelect = 'none';
                    
                    // Force canvas to stay exactly the same size
                    yearCanvas.width = STATIC_WIDTH;
                    yearCanvas.height = STATIC_HEIGHT;
                    yearCanvas.style.width = STATIC_WIDTH + 'px';
                    yearCanvas.style.height = STATIC_HEIGHT + 'px';
                    yearCanvas.style.maxWidth = STATIC_WIDTH + 'px';
                    yearCanvas.style.maxHeight = STATIC_HEIGHT + 'px';
                    
                    // Disable all mouse events on product canvas
                    productCanvas.style.pointerEvents = 'none';
                    productCanvas.style.touchAction = 'none';
                    productCanvas.style.userSelect = 'none';
                    productCanvas.style.webkitUserSelect = 'none';
                    productCanvas.style.mozUserSelect = 'none';
                    productCanvas.style.msUserSelect = 'none';
                    
                    // Force product canvas to stay exactly the same size
                    productCanvas.width = STATIC_WIDTH;
                    productCanvas.height = STATIC_HEIGHT;
                    productCanvas.style.width = STATIC_WIDTH + 'px';
                    productCanvas.style.height = STATIC_HEIGHT + 'px';
                    productCanvas.style.maxWidth = STATIC_WIDTH + 'px';
                    productCanvas.style.maxHeight = STATIC_HEIGHT + 'px';
                }, 100);
            }

            function updateTable(data) {
                const tbody = document.getElementById('summary-table-body');
                tbody.innerHTML = '';

                if (data.summary && data.summary.length > 0) {
                    data.summary.forEach(row => {
                        const tr = document.createElement('tr');
                        tr.className = 'hover:bg-gray-50';
                        tr.innerHTML = `
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${row.year || '-'}</td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${row.final_product || '-'}</td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${row.avg_yield?.toFixed(2) || '0.00'} ц/га</td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${row.max_yield?.toFixed(2) || '0.00'} ц/га</td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${row.count || 0}</td>
                        `;
                        tbody.appendChild(tr);
                    });
                } else {
                    tbody.innerHTML = '<tr><td colspan="5" class="px-6 py-4 text-center text-gray-500">Нет данных для отображения</td></tr>';
                }
            }

            function updateFilters(data) {
                // Update year filter
                const yearSelect = document.getElementById('year-filter');
                const currentYear = yearSelect.value;
                yearSelect.innerHTML = '<option value="">Все годы</option>';
                
                if (data.years) {
                    data.years.forEach(year => {
                        const option = document.createElement('option');
                        option.value = year;
                        option.textContent = year;
                        if (year == currentYear) option.selected = true;
                        yearSelect.appendChild(option);
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

            function exportTable() {
                const table = document.getElementById('summary-table-body');
                let csv = 'Год,Конечный продукт,Средняя урожайность,Максимальная урожайность,Количество записей\\n';
                
                table.querySelectorAll('tr').forEach(row => {
                    const cells = row.querySelectorAll('td');
                    if (cells.length > 0) {
                        const rowData = Array.from(cells).map(cell => cell.textContent.trim()).join(',');
                        csv += rowData + '\\n';
                    }
                });
                
                const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
                const link = document.createElement('a');
                link.href = URL.createObjectURL(blob);
                link.download = 'yield-comparison-report.csv';
                link.click();
            }

            // Force STATIC chart dimensions function
            function forceChartDimensions() {
                const yearCanvas = document.getElementById('yield-by-year-chart');
                const productCanvas = document.getElementById('yield-by-product-chart');
                const yearContainer = yearCanvas ? yearCanvas.parentElement : null;
                const productContainer = productCanvas ? productCanvas.parentElement : null;
                
                // Force STATIC container dimensions
                if (yearContainer) {
                    yearContainer.style.width = '100%';
                    yearContainer.style.maxWidth = '100%';
                    yearContainer.style.height = '450px'; // Fixed height
                    yearContainer.style.overflow = 'hidden';
                    yearContainer.style.position = 'relative';
                }
                
                if (productContainer) {
                    productContainer.style.width = '100%';
                    productContainer.style.maxWidth = '100%';
                    productContainer.style.height = '450px'; // Fixed height
                    productContainer.style.overflow = 'hidden';
                    productContainer.style.position = 'relative';
                }
                
                // Force STATIC canvas dimensions
                if (yearCanvas) {
                    yearCanvas.width = STATIC_WIDTH;
                    yearCanvas.height = STATIC_HEIGHT;
                    yearCanvas.style.width = STATIC_WIDTH + 'px';
                    yearCanvas.style.height = STATIC_HEIGHT + 'px';
                    yearCanvas.style.maxWidth = STATIC_WIDTH + 'px';
                    yearCanvas.style.maxHeight = STATIC_HEIGHT + 'px';
                    yearCanvas.style.display = 'block';
                    yearCanvas.style.position = 'absolute';
                    yearCanvas.style.top = '50px';
                    yearCanvas.style.left = '0';
                    yearCanvas.style.right = '0';
                }
                
                if (productCanvas) {
                    productCanvas.width = STATIC_WIDTH;
                    productCanvas.height = STATIC_HEIGHT;
                    productCanvas.style.width = STATIC_WIDTH + 'px';
                    productCanvas.style.height = STATIC_HEIGHT + 'px';
                    productCanvas.style.maxWidth = STATIC_WIDTH + 'px';
                    productCanvas.style.maxHeight = STATIC_HEIGHT + 'px';
                    productCanvas.style.display = 'block';
                    productCanvas.style.position = 'absolute';
                    productCanvas.style.top = '50px';
                    productCanvas.style.left = '0';
                    productCanvas.style.right = '0';
                }
            }

            // STATIC DIMENSIONS - NO CALCULATIONS
            const STATIC_WIDTH = 400;
            const STATIC_HEIGHT = 300;

            // Force STATIC dimensions immediately when page loads
            function initializeChartConstraints() {
                const yearCanvas = document.getElementById('yield-by-year-chart');
                const productCanvas = document.getElementById('yield-by-product-chart');
                const yearContainer = yearCanvas ? yearCanvas.parentElement : null;
                const productContainer = productCanvas ? productCanvas.parentElement : null;
                
                // Set STATIC container constraints
                if (yearContainer) {
                    yearContainer.style.width = '100%';
                    yearContainer.style.maxWidth = '100%';
                    yearContainer.style.height = '450px'; // Fixed height
                    yearContainer.style.overflow = 'hidden';
                    yearContainer.style.position = 'relative';
                }
                
                if (productContainer) {
                    productContainer.style.width = '100%';
                    productContainer.style.maxWidth = '100%';
                    productContainer.style.height = '450px'; // Fixed height
                    productContainer.style.overflow = 'hidden';
                    productContainer.style.position = 'relative';
                }
                
                // Set STATIC canvas constraints
                if (yearCanvas) {
                    yearCanvas.width = STATIC_WIDTH;
                    yearCanvas.height = STATIC_HEIGHT;
                    yearCanvas.style.width = STATIC_WIDTH + 'px';
                    yearCanvas.style.height = STATIC_HEIGHT + 'px';
                    yearCanvas.style.maxWidth = STATIC_WIDTH + 'px';
                    yearCanvas.style.maxHeight = STATIC_HEIGHT + 'px';
                    yearCanvas.style.display = 'block';
                    yearCanvas.style.position = 'absolute';
                    yearCanvas.style.top = '50px';
                    yearCanvas.style.left = '0';
                    yearCanvas.style.right = '0';
                }
                
                if (productCanvas) {
                    productCanvas.width = STATIC_WIDTH;
                    productCanvas.height = STATIC_HEIGHT;
                    productCanvas.style.width = STATIC_WIDTH + 'px';
                    productCanvas.style.height = STATIC_HEIGHT + 'px';
                    productCanvas.style.maxWidth = STATIC_WIDTH + 'px';
                    productCanvas.style.maxHeight = STATIC_HEIGHT + 'px';
                    productCanvas.style.display = 'block';
                    productCanvas.style.position = 'absolute';
                    productCanvas.style.top = '50px';
                    productCanvas.style.left = '0';
                    productCanvas.style.right = '0';
                }
            }

            // Load data on page load
            document.addEventListener('DOMContentLoaded', function() {
                // Set constraints immediately before loading data
                initializeChartConstraints();
                
                // Load report data
                loadReport();
                
                // Force dimensions after load
                setTimeout(forceChartDimensions, 100);
                setTimeout(forceChartDimensions, 500);
            });
            
            // Force dimensions on window resize
            window.addEventListener('resize', function() {
                setTimeout(forceChartDimensions, 100);
            });
        </script>
    </body>
    </html>
    """
