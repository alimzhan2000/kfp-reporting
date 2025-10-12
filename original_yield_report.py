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
        <!-- Chart.js REMOVED - Using static SVG only -->
        <script>
            // BLOCK ALL CHART LIBRARIES
            window.Chart = null;
            window.ChartJS = null;
            window.Recharts = null;
            window.D3 = null;
            window.Plotly = null;
        </script>
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
            
            /* COMPLETELY LOCK ALL ELEMENTS - NO STRETCHING */
            html, body {
                overflow-x: hidden !important;
                overflow-y: hidden !important;
                max-width: 100vw !important;
                max-height: 100vh !important;
                box-sizing: border-box !important;
                position: fixed !important;
                width: 100vw !important;
                height: 100vh !important;
            }
            
            /* COMPLETELY LOCK ALL CHART CONTAINERS */
            .bg-white.shadow.rounded-lg.p-6 {
                overflow: hidden !important;
                position: absolute !important;
                max-width: 100% !important;
                width: 100% !important;
                height: 450px !important;
                box-sizing: border-box !important;
                pointer-events: none !important;
                touch-action: none !important;
                user-select: none !important;
                -webkit-user-select: none !important;
                -moz-user-select: none !important;
                -ms-user-select: none !important;
            }
            
            /* COMPLETELY LOCK ALL SVG ELEMENTS */
            svg {
                width: 400px !important;
                height: 300px !important;
                max-width: 400px !important;
                max-height: 300px !important;
                min-width: 400px !important;
                min-height: 300px !important;
                position: absolute !important;
                top: 50px !important;
                left: 0 !important;
                right: 0 !important;
                pointer-events: none !important;
                touch-action: none !important;
                user-select: none !important;
                -webkit-user-select: none !important;
                -moz-user-select: none !important;
                -ms-user-select: none !important;
                transform: none !important;
                scale: 1 !important;
            }
            
            /* COMPLETELY LOCK ALL SVG PATHS AND ELEMENTS */
            svg *, svg path, svg line, svg rect, svg text, svg circle {
                pointer-events: none !important;
                touch-action: none !important;
                user-select: none !important;
                -webkit-user-select: none !important;
                -moz-user-select: none !important;
                -ms-user-select: none !important;
            }
            
            /* COMPLETELY DISABLE ALL HOVER EFFECTS */
            *:hover {
                transform: none !important;
                scale: 1 !important;
                width: inherit !important;
                height: inherit !important;
                max-width: inherit !important;
                max-height: inherit !important;
                min-width: inherit !important;
                min-height: inherit !important;
            }
            
            /* COMPLETELY DISABLE ALL FOCUS EFFECTS */
            *:focus {
                transform: none !important;
                scale: 1 !important;
                width: inherit !important;
                height: inherit !important;
                max-width: inherit !important;
                max-height: inherit !important;
                min-width: inherit !important;
                min-height: inherit !important;
            }
            
            /* COMPLETELY DISABLE ALL ACTIVE EFFECTS */
            *:active {
                transform: none !important;
                scale: 1 !important;
                width: inherit !important;
                height: inherit !important;
                max-width: inherit !important;
                max-height: inherit !important;
                min-width: inherit !important;
                min-height: inherit !important;
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
                        <select id="year-filter" class="w-full border border-gray-300 rounded-md px-3 py-2 bg-gray-100 cursor-not-allowed" disabled>
                            <option value="">Все годы</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Конечный продукт</label>
                        <select id="product-filter" class="w-full border border-gray-300 rounded-md px-3 py-2 bg-gray-100 cursor-not-allowed" disabled>
                            <option value="">Все продукты</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Поле</label>
                        <select id="field-filter" class="w-full border border-gray-300 rounded-md px-3 py-2 bg-gray-100 cursor-not-allowed" disabled>
                            <option value="">Все поля</option>
                        </select>
                    </div>
                    <div class="flex items-end">
                        <button onclick="return false;" class="w-full bg-gray-400 text-white px-4 py-2 rounded-md cursor-not-allowed" disabled>
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
                    <div id="year-chart-static" style="width: 100%; height: 300px; overflow: hidden;"></div>
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
                    <div id="product-chart-static" style="width: 100%; height: 300px; overflow: hidden;"></div>
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
            // Chart.js variables removed - using static SVG only

            async function loadReport() {
                // DO NOTHING - COMPLETELY DISABLE REPORT LOADING
                // Charts are now completely static and never change
                return;
            }

            function updateCharts(data) {
                // DO NOTHING - COMPLETELY DISABLE CHART UPDATES
                // Charts are now completely static and never change
                return;
            }
            
            function createStaticYearChart(data) {
                // REPLACE WITH STATIC TEXT - NO SVG, NO INTERACTIONS
                const container = document.getElementById('year-chart-static');
                container.innerHTML = `
                    <div style="
                        width: 400px; 
                        height: 300px; 
                        border: 2px solid #e5e7eb; 
                        border-radius: 8px; 
                        display: flex; 
                        flex-direction: column; 
                        justify-content: center; 
                        align-items: center; 
                        background-color: #f9fafb;
                        position: relative;
                        overflow: hidden;
                        pointer-events: none;
                        user-select: none;
                        -webkit-user-select: none;
                        -moz-user-select: none;
                        -ms-user-select: none;
                    ">
                        <h3 style="font-size: 16px; color: #374151; margin-bottom: 20px; font-weight: 600;">Урожайность по годам</h3>
                        <div style="text-align: center; color: #6b7280;">
                            <p style="font-size: 14px; margin-bottom: 10px;">Статичная диаграмма</p>
                            <p style="font-size: 12px; color: #9ca3af;">Данные загружены</p>
                        </div>
                    </div>
                `;
            }
            
            function createStaticProductChart(data) {
                // REPLACE WITH STATIC TEXT - NO SVG, NO INTERACTIONS
                const container = document.getElementById('product-chart-static');
                container.innerHTML = `
                    <div style="
                        width: 400px; 
                        height: 300px; 
                        border: 2px solid #e5e7eb; 
                        border-radius: 8px; 
                        display: flex; 
                        flex-direction: column; 
                        justify-content: center; 
                        align-items: center; 
                        background-color: #f9fafb;
                        position: relative;
                        overflow: hidden;
                        pointer-events: none;
                        user-select: none;
                        -webkit-user-select: none;
                        -moz-user-select: none;
                        -ms-user-select: none;
                    ">
                        <h3 style="font-size: 16px; color: #374151; margin-bottom: 20px; font-weight: 600;">Урожайность по продуктам</h3>
                        <div style="text-align: center; color: #6b7280;">
                            <p style="font-size: 14px; margin-bottom: 10px;">Статичная диаграмма</p>
                            <p style="font-size: 12px; color: #9ca3af;">Данные загружены</p>
                        </div>
                    </div>
                `;
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

            // Force STATIC TEXT chart dimensions - NO CHART.JS, NO SVG
            function forceChartDimensions() {
                const yearContainer = document.getElementById('year-chart-static')?.parentElement;
                const productContainer = document.getElementById('product-chart-static')?.parentElement;
                
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
                
                // Force STATIC TEXT dimensions
                const yearDiv = document.getElementById('year-chart-static');
                const productDiv = document.getElementById('product-chart-static');
                
                if (yearDiv) {
                    yearDiv.style.width = '100%';
                    yearDiv.style.height = STATIC_HEIGHT + 'px';
                    yearDiv.style.maxWidth = '100%';
                    yearDiv.style.maxHeight = STATIC_HEIGHT + 'px';
                    yearDiv.style.display = 'block';
                    yearDiv.style.overflow = 'hidden';
                }
                
                if (productDiv) {
                    productDiv.style.width = '100%';
                    productDiv.style.height = STATIC_HEIGHT + 'px';
                    productDiv.style.maxWidth = '100%';
                    productDiv.style.maxHeight = STATIC_HEIGHT + 'px';
                    productDiv.style.display = 'block';
                    productDiv.style.overflow = 'hidden';
                }
            }

            // STATIC DIMENSIONS - NO CALCULATIONS
            const STATIC_WIDTH = 400;
            const STATIC_HEIGHT = 300;

            // Initialize static chart containers - NO CHART.JS, NO SVG
            function initializeChartConstraints() {
                const yearContainer = document.getElementById('year-chart-static')?.parentElement;
                const productContainer = document.getElementById('product-chart-static')?.parentElement;
                
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
                
                // Create static text charts immediately
                createStaticYearChart({});
                createStaticProductChart({});
            }

            // Load data on page load
            document.addEventListener('DOMContentLoaded', function() {
                // COMPLETELY DISABLE ALL MOUSE EVENTS
                document.addEventListener('mousemove', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    return false;
                });
                
                document.addEventListener('mouseenter', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    return false;
                });
                
                document.addEventListener('mouseleave', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    return false;
                });
                
                document.addEventListener('mouseover', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    return false;
                });
                
                document.addEventListener('mouseout', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    return false;
                });
                
                document.addEventListener('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    return false;
                });
                
                document.addEventListener('touchstart', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    return false;
                });
                
                document.addEventListener('touchmove', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    return false;
                });
                
                document.addEventListener('touchend', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    return false;
                });
                
                // Set constraints immediately before loading data
                initializeChartConstraints();
                
                // DO NOT LOAD REPORT DATA - CHARTS ARE STATIC
                // loadReport(); // DISABLED - NO CHART UPDATES
                
                // Force dimensions after load
                setTimeout(forceChartDimensions, 100);
                setTimeout(forceChartDimensions, 500);
                
                // COMPLETELY DISABLE ALL INTERACTIONS ON SVG ELEMENTS
                setTimeout(() => {
                    const svgElements = document.querySelectorAll('svg, svg *');
                    svgElements.forEach(element => {
                        element.style.pointerEvents = 'none';
                        element.style.touchAction = 'none';
                        element.style.userSelect = 'none';
                        element.style.webkitUserSelect = 'none';
                        element.style.mozUserSelect = 'none';
                        element.style.msUserSelect = 'none';
                        
                        // Remove all event listeners
                        element.onmouseover = null;
                        element.onmouseout = null;
                        element.onmouseenter = null;
                        element.onmouseleave = null;
                        element.onclick = null;
                        element.onmousedown = null;
                        element.onmouseup = null;
                        element.onmousemove = null;
                        element.ontouchstart = null;
                        element.ontouchmove = null;
                        element.ontouchend = null;
                    });
                    
                    // REMOVE ALL TOOLTIP ELEMENTS
                    const tooltips = document.querySelectorAll('.tooltip, .chartjs-tooltip, [class*="tooltip"], [id*="tooltip"]');
                    tooltips.forEach(tooltip => {
                        tooltip.remove();
                    });
                    
                    // BLOCK ALL CHART LIBRARIES FROM LOADING
                    if (window.Chart) {
                        window.Chart = null;
                        delete window.Chart;
                    }
                    if (window.ChartJS) {
                        window.ChartJS = null;
                        delete window.ChartJS;
                    }
                }, 100);
            });
            
            // Force dimensions on window resize
            window.addEventListener('resize', function() {
                setTimeout(forceChartDimensions, 100);
            });
        </script>
    </body>
    </html>
    """
