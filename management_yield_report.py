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
        <!-- Chart.js REMOVED - Using static text only -->
        <style>
            /* Prevent table from stretching the page */
            body {
                overflow-x: hidden;
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
                    <div id="year-chart-static" style="width: 100%; height: 300px; overflow: hidden; border: 2px solid #e5e7eb; border-radius: 8px; display: flex; flex-direction: column; justify-content: center; align-items: center; background-color: #f9fafb; pointer-events: none; user-select: none;">
                        <h3 style="font-size: 16px; color: #374151; margin-bottom: 20px; font-weight: 600;">Урожайность по годам</h3>
                        <div style="text-align: center; color: #6b7280;">
                            <p style="font-size: 14px; margin-bottom: 10px;">Статичная диаграмма</p>
                            <p style="font-size: 12px; color: #9ca3af;">Данные загружены</p>
                        </div>
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
                    <div id="product-chart-static" style="width: 100%; height: 300px; overflow: hidden; border: 2px solid #e5e7eb; border-radius: 8px; display: flex; flex-direction: column; justify-content: center; align-items: center; background-color: #f9fafb; pointer-events: none; user-select: none;">
                        <h3 style="font-size: 16px; color: #374151; margin-bottom: 20px; font-weight: 600;">Урожайность по продуктам</h3>
                        <div style="text-align: center; color: #6b7280;">
                            <p style="font-size: 14px; margin-bottom: 10px;">Статичная диаграмма</p>
                            <p style="font-size: 12px; color: #9ca3af;">Данные загружены</p>
                        </div>
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
                // Create static SVG charts - no stretching, no interactions
                createStaticYearChart(data);
                createStaticProductChart(data);
            }
            
            function createStaticYearChart(data) {
                const container = document.getElementById('year-chart-static');
                if (!container) return;
                
                const width = 400;
                const height = 300;
                const years = data.years || [];
                const yields = data.yield_by_year || [];
                
                let svgContent = '';
                
                if (years.length > 0 && yields.length > 0) {
                    // Calculate chart dimensions
                    const padding = 40;
                    const chartWidth = width - 2 * padding;
                    const chartHeight = height - 2 * padding;
                    
                    const maxY = Math.max(...yields);
                    const minY = Math.min(...yields);
                    const range = maxY - minY || 1;
                    
                    // Draw axes
                    svgContent += `<line x1="${padding}" y1="${height - padding}" x2="${width - padding}" y2="${height - padding}" stroke="#666" stroke-width="2"/>`;
                    svgContent += `<line x1="${padding}" y1="${padding}" x2="${padding}" y2="${height - padding}" stroke="#666" stroke-width="2"/>`;
                    
                    // Draw data line
                    let pathData = '';
                    years.forEach((year, index) => {
                        const x = padding + (index * chartWidth / (years.length - 1));
                        const y = height - padding - ((yields[index] - minY) / range) * chartHeight;
                        if (index === 0) {
                            pathData += `M ${x} ${y}`;
                        } else {
                            pathData += ` L ${x} ${y}`;
                        }
                    });
                    
                    svgContent += `<path d="${pathData}" stroke="rgb(34, 197, 94)" stroke-width="3" fill="none"/>`;
                    
                    // Add data points
                    years.forEach((year, index) => {
                        const x = padding + (index * chartWidth / (years.length - 1));
                        const y = height - padding - ((yields[index] - minY) / range) * chartHeight;
                        svgContent += `<circle cx="${x}" cy="${y}" r="4" fill="rgb(34, 197, 94)"/>`;
                    });
                    
                    // Add title
                    svgContent += `<text x="${width/2}" y="20" text-anchor="middle" font-size="14" fill="#333">Урожайность по годам</text>`;
                    
                } else {
                    // No data message
                    svgContent += `<text x="${width/2}" y="${height/2}" text-anchor="middle" font-size="14" fill="#999">Нет данных для отображения</text>`;
                }
                
                container.innerHTML = `
                    <svg width="${width}" height="${height}" style="width: ${width}px; height: ${height}px; max-width: ${width}px; max-height: ${height}px; display: block; pointer-events: none; user-select: none;">
                        ${svgContent}
                    </svg>
                `;
            }
            
            function createStaticProductChart(data) {
                const container = document.getElementById('product-chart-static');
                if (!container) return;
                
                const width = 400;
                const height = 300;
                const products = data.products || [];
                const yields = data.yield_by_product || [];
                
                let svgContent = '';
                
                if (products.length > 0 && yields.length > 0) {
                    // Calculate chart dimensions
                    const padding = 40;
                    const chartWidth = width - 2 * padding;
                    const chartHeight = height - 2 * padding;
                    
                    const maxY = Math.max(...yields);
                    const colors = ['#3b82f6', '#22c55e', '#fbbf24', '#ef4444', '#9333ea', '#ec4899', '#06b6d4'];
                    
                    // Draw axes
                    svgContent += `<line x1="${padding}" y1="${height - padding}" x2="${width - padding}" y2="${height - padding}" stroke="#666" stroke-width="2"/>`;
                    svgContent += `<line x1="${padding}" y1="${padding}" x2="${padding}" y2="${height - padding}" stroke="#666" stroke-width="2"/>`;
                    
                    // Draw bars
                    const barWidth = chartWidth / products.length * 0.8;
                    const barSpacing = chartWidth / products.length;
                    
                    products.forEach((product, index) => {
                        const barHeight = (yields[index] / maxY) * chartHeight;
                        const x = padding + (index * barSpacing) + (barSpacing - barWidth) / 2;
                        const y = height - padding - barHeight;
                        
                        svgContent += `<rect x="${x}" y="${y}" width="${barWidth}" height="${barHeight}" fill="${colors[index % colors.length]}" opacity="0.8"/>`;
                    });
                    
                    // Add title
                    svgContent += `<text x="${width/2}" y="20" text-anchor="middle" font-size="14" fill="#333">Урожайность по продуктам</text>`;
                    
                } else {
                    // No data message
                    svgContent += `<text x="${width/2}" y="${height/2}" text-anchor="middle" font-size="14" fill="#999">Нет данных для отображения</text>`;
                }
                
                container.innerHTML = `
                    <svg width="${width}" height="${height}" style="width: ${width}px; height: ${height}px; max-width: ${width}px; max-height: ${height}px; display: block; pointer-events: none; user-select: none;">
                        ${svgContent}
                    </svg>
                `;
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

            // Load data on page load
            document.addEventListener('DOMContentLoaded', function() {
                // Initialize static charts with empty data
                createStaticYearChart({});
                createStaticProductChart({});
                
                // Load report data
                loadReport();
            });
        </script>
    </body>
    </html>
    """
