"""
Отчет производительности сортов для менеджмента
"""
from django.http import HttpResponse

def get_variety_performance_report():
    """Возвращает отчет производительности сортов для менеджмента"""
    return """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>KFP Reporting - Производительность сортов</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
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
            
            /* Set specific column widths */
            table th:nth-child(1), table td:nth-child(1) {
                width: 25%;
                max-width: 200px;
            }
            
            table th:nth-child(2), table td:nth-child(2) {
                width: 25%;
                max-width: 200px;
            }
            
            table th:nth-child(3), table td:nth-child(3) {
                width: 15%;
            }
            
            table th:nth-child(4), table td:nth-child(4) {
                width: 15%;
            }
            
            table th:nth-child(5), table td:nth-child(5) {
                width: 10%;
            }
            
            table th:nth-child(6), table td:nth-child(6) {
                width: 10%;
            }
            
            /* Ensure charts don't overflow */
            canvas {
                max-width: 100% !important;
                height: auto !important;
            }
            
            /* Prevent chart containers from expanding */
            .bg-white.shadow.rounded-lg.p-6 {
                overflow: hidden;
                position: relative;
            }
            
            /* Force chart canvas to stay within bounds */
            #variety-performance-chart,
            #variety-by-product-chart {
                max-width: 100% !important;
                max-height: 400px !important;
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
                        <a href="/reports/variety-performance/" class="text-blue-600 hover:text-blue-800 px-3 py-2 rounded font-medium">Производительность сортов</a>
                        <a href="/admin/" class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded">Admin</a>
                    </div>
                </div>
            </div>
        </nav>

        <!-- Main Content -->
        <div class="max-w-7xl mx-auto px-4 py-8">
            <div class="mb-8">
                <h1 class="text-2xl font-bold text-gray-900">Производительность сортов</h1>
                <p class="mt-1 text-sm text-gray-500">
                    Анализ производительности сортов в рамках различных культур и полей
                </p>
            </div>

            <!-- Filters -->
            <div class="bg-white shadow rounded-lg p-6 mb-8">
                <h3 class="text-lg font-medium text-gray-900 mb-4">Фильтры</h3>
                <div class="grid grid-cols-1 gap-4 md:grid-cols-4">
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
                <!-- Variety Performance Chart -->
                <div class="bg-white shadow rounded-lg p-6">
                    <div class="flex items-center justify-between mb-4">
                        <h3 class="text-lg font-medium text-gray-900">Топ сортов по урожайности</h3>
                        <div class="flex space-x-2">
                            <button onclick="downloadChart('variety-performance-chart', 'variety-performance.png')" class="text-gray-400 hover:text-gray-600">
                                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                                </svg>
                            </button>
                        </div>
                    </div>
                    <canvas id="variety-performance-chart" width="400" height="300"></canvas>
                </div>

                <!-- Variety by Product Chart -->
                <div class="bg-white shadow rounded-lg p-6">
                    <div class="flex items-center justify-between mb-4">
                        <h3 class="text-lg font-medium text-gray-900">Сорта по продуктам</h3>
                        <div class="flex space-x-2">
                            <button onclick="downloadChart('variety-by-product-chart', 'variety-by-product.png')" class="text-gray-400 hover:text-gray-600">
                                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                                </svg>
                            </button>
                        </div>
                    </div>
                    <canvas id="variety-by-product-chart" width="400" height="300"></canvas>
                </div>
            </div>

            <!-- Variety Performance Table -->
            <div class="mt-8 bg-white shadow rounded-lg p-6">
                <div class="flex items-center justify-between mb-4">
                    <h3 class="text-lg font-medium text-gray-900">Детальный анализ сортов</h3>
                    <div class="flex space-x-2">
                        <button onclick="exportTable('variety-performance-table')" class="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 focus:ring-2 focus:ring-green-500 focus:ring-offset-2 transition-colors">
                            <svg class="w-4 h-4 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                            </svg>
                            Экспорт CSV
                        </button>
                    </div>
                </div>
                <div class="overflow-x-auto">
                    <table id="variety-performance-table" class="min-w-full divide-y divide-gray-200">
                        <thead class="bg-gray-50">
                            <tr>
                                <th class="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Сорт</th>
                                <th class="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Продукт</th>
                                <th class="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap">Средняя (ц/га)</th>
                                <th class="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap">Макс (ц/га)</th>
                                <th class="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap">Полей</th>
                                <th class="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Рейтинг</th>
                            </tr>
                        </thead>
                        <tbody id="variety-performance-table-body" class="bg-white divide-y divide-gray-200">
                            <tr>
                                <td colspan="6" class="px-3 py-4 text-center text-gray-500">Загрузите данные для отображения таблицы</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <script>
            let varietyPerformanceChart, varietyByProductChart;

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

                    const params = new URLSearchParams();
                    if (yearFrom) params.append('year_from', yearFrom);
                    if (yearTo) params.append('year_to', yearTo);
                    if (product) params.append('final_product', product);

                    const response = await fetch(`/api/reports/variety-performance/?${params}`);
                    
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    
                    const data = await response.json();
                    console.log('Received variety performance data:', data);

                    updateCharts(data);
                    updateVarietyTable(data);
                    updateFilters(data);

                } catch (error) {
                    console.error('Error loading variety performance report:', error);
                    errorState.classList.remove('hidden');
                    document.getElementById('error-message').textContent = error.message;
                } finally {
                    loadingState.classList.add('hidden');
                    chartsContainer.classList.remove('hidden');
                }
            }

            function updateCharts(data) {
                // Variety Performance Chart
                const varietyCtx = document.getElementById('variety-performance-chart').getContext('2d');
                if (varietyPerformanceChart) varietyPerformanceChart.destroy();
                
                varietyPerformanceChart = new Chart(varietyCtx, {
                    type: 'bar',
                    data: {
                        labels: data.variety_names || [],
                        datasets: [{
                            label: 'Урожайность (ц/га)',
                            data: data.variety_yields || [],
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
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {
                            y: {
                                beginAtZero: true,
                                title: {
                                    display: true,
                                    text: 'Урожайность (ц/га)'
                                }
                            }
                        },
                        plugins: {
                            legend: {
                                display: true,
                                position: 'top'
                            },
                            tooltip: {
                                enabled: true,
                                mode: 'nearest',
                                intersect: true,
                                position: 'average',
                                callbacks: {
                                    title: function(context) {
                                        let label = context[0].label || '';
                                        // Truncate long labels in tooltip
                                        if (label.length > 40) {
                                            return label.substring(0, 37) + '...';
                                        }
                                        return label;
                                    }
                                },
                                bodyFont: {
                                    size: 12
                                },
                                titleFont: {
                                    size: 12
                                },
                                boxPadding: 4,
                                padding: 8,
                                displayColors: true,
                                backgroundColor: 'rgba(0, 0, 0, 0.8)',
                                maxWidth: 300
                            }
                        }
                    }
                });

                // Variety by Product Chart
                const productCtx = document.getElementById('variety-by-product-chart').getContext('2d');
                if (varietyByProductChart) varietyByProductChart.destroy();
                
                varietyByProductChart = new Chart(productCtx, {
                    type: 'doughnut',
                    data: {
                        labels: data.product_labels || [],
                        datasets: [{
                            data: data.product_data || [],
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
                            borderWidth: 2
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: {
                                display: true,
                                position: 'bottom',
                                labels: {
                                    boxWidth: 12,
                                    padding: 8,
                                    font: {
                                        size: 11
                                    },
                                    generateLabels: function(chart) {
                                        const data = chart.data;
                                        if (data.labels.length && data.datasets.length) {
                                            return data.labels.map((label, i) => {
                                                // Truncate long labels in legend
                                                let truncatedLabel = label;
                                                if (label.length > 25) {
                                                    truncatedLabel = label.substring(0, 22) + '...';
                                                }
                                                return {
                                                    text: truncatedLabel,
                                                    fillStyle: data.datasets[0].backgroundColor[i],
                                                    hidden: false,
                                                    index: i
                                                };
                                            });
                                        }
                                        return [];
                                    }
                                }
                            },
                            tooltip: {
                                enabled: true,
                                callbacks: {
                                    label: function(context) {
                                        let label = context.label || '';
                                        // Truncate long labels in tooltip
                                        if (label.length > 30) {
                                            label = label.substring(0, 27) + '...';
                                        }
                                        if (context.parsed !== null) {
                                            label += ': ' + context.parsed;
                                        }
                                        return label;
                                    }
                                },
                                bodyFont: {
                                    size: 12
                                },
                                padding: 8,
                                backgroundColor: 'rgba(0, 0, 0, 0.8)',
                                maxWidth: 250
                            }
                        }
                    }
                });
            }

            function updateVarietyTable(data) {
                const tbody = document.getElementById('variety-performance-table-body');
                tbody.innerHTML = '';

                if (data.variety_data && data.variety_data.length > 0) {
                    data.variety_data.forEach((row, index) => {
                        const tr = document.createElement('tr');
                        tr.className = 'hover:bg-gray-50';
                        
                        // Определяем рейтинг
                        let rating = '';
                        let ratingClass = '';
                        if (index < 3) {
                            rating = `${index + 1} место`;
                            ratingClass = index === 0 ? 'text-yellow-600 bg-yellow-100' : 
                                         index === 1 ? 'text-gray-600 bg-gray-100' : 
                                         'text-orange-600 bg-orange-100';
                        } else {
                            rating = 'Средний';
                            ratingClass = 'text-blue-600 bg-blue-100';
                        }
                        
                        tr.innerHTML = `
                            <td class="px-3 py-3 text-sm font-medium text-gray-900 max-w-xs truncate" title="${row.variety || '-'}">${row.variety || '-'}</td>
                            <td class="px-3 py-3 text-sm text-gray-900 max-w-xs truncate" title="${row.final_product || '-'}">${row.final_product || '-'}</td>
                            <td class="px-3 py-3 whitespace-nowrap text-sm text-gray-900">${row.avg_yield?.toFixed(1) || '0.0'}</td>
                            <td class="px-3 py-3 whitespace-nowrap text-sm text-gray-900">${row.max_yield?.toFixed(1) || '0.0'}</td>
                            <td class="px-3 py-3 whitespace-nowrap text-sm text-gray-900 text-center">${row.fields || 0}</td>
                            <td class="px-3 py-3 whitespace-nowrap">
                                <span class="inline-flex px-2 py-1 text-xs font-semibold rounded-full ${ratingClass}">
                                    ${rating}
                                </span>
                            </td>
                        `;
                        tbody.appendChild(tr);
                    });
                } else {
                    tbody.innerHTML = '<tr><td colspan="6" class="px-3 py-4 text-center text-gray-500">Нет данных для отображения</td></tr>';
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
                loadReport();
            });
        </script>
    </body>
    </html>
    """
