from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def minimal_pandas_test_page(request):
    """Минимальная тестовая страница pandas"""
    html_content = """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>KFP Reporting - Минимальный тест pandas</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-50">
        <nav class="bg-white shadow">
            <div class="max-w-7xl mx-auto px-4">
                <div class="flex justify-between items-center py-4">
                    <div class="flex items-center">
                        <div class="text-2xl mr-3">🔬</div>
                        <h1 class="text-gray-900 text-xl font-bold">Минимальный тест pandas</h1>
                    </div>
                    <div class="flex items-center space-x-4">
                        <a href="/" class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded">Дашборд</a>
                        <a href="/pandas-isolation-test/" class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded">Изоляция</a>
                        <a href="/admin/" class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded">Admin</a>
                    </div>
                </div>
            </div>
        </nav>

        <div class="max-w-4xl mx-auto px-4 py-8">
            <div class="mb-8">
                <h1 class="text-2xl font-bold text-gray-900">Минимальный тест pandas</h1>
                <p class="mt-1 text-sm text-gray-500">Только импорт и создание DataFrame</p>
            </div>

            <div class="bg-white shadow rounded-lg p-8">
                <div class="text-center">
                    <button id="run-test" class="bg-blue-600 text-white px-6 py-3 rounded-md hover:bg-blue-700 text-lg font-medium">
                        Запустить минимальный тест
                    </button>
                </div>
                
                <div id="result" class="mt-6 hidden">
                    <pre id="result-content" class="bg-gray-100 p-4 rounded-lg overflow-auto max-h-96 text-sm"></pre>
                </div>
            </div>

            <div class="mt-8 bg-white shadow rounded-lg p-6">
                <h3 class="text-lg font-medium text-gray-900 mb-4">Что делает минимальный тест</h3>
                <div class="space-y-3 text-sm text-gray-600">
                    <p>• Импорт pandas</p>
                    <p>• Импорт openpyxl</p>
                    <p>• Создание простого DataFrame</p>
                    <p>• Проверка версий</p>
                    <p>• БЕЗ работы с файлами</p>
                </div>
            </div>
        </div>

        <script>
            const runTestButton = document.getElementById('run-test');
            const resultDiv = document.getElementById('result');
            const resultContent = document.getElementById('result-content');

            runTestButton.addEventListener('click', async () => {
                resultDiv.classList.remove('hidden');
                resultContent.textContent = 'Запуск минимального теста...';
                runTestButton.disabled = true;
                runTestButton.textContent = 'Тестирование...';

                try {
                    console.log('Running minimal pandas test...');
                    const response = await fetch('/api/upload/minimal-pandas-test/', {
                        method: 'POST'
                    });

                    const result = await response.json();
                    console.log('Minimal pandas test result:', result);

                    resultContent.textContent = JSON.stringify(result, null, 2);
                } catch (error) {
                    resultContent.textContent = 'Ошибка: ' + error.message;
                    console.error('Minimal pandas test error:', error);
                } finally {
                    runTestButton.disabled = false;
                    runTestButton.textContent = 'Запустить минимальный тест';
                }
            });
        </script>
    </body>
    </html>
    """
    return HttpResponse(html_content, content_type="text/html")
