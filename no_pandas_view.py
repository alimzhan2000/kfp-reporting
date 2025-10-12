from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def no_pandas_test_page(request):
    """Тестовая страница без pandas"""
    html_content = """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>KFP Reporting - Тест без pandas</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-50">
        <nav class="bg-white shadow">
            <div class="max-w-7xl mx-auto px-4">
                <div class="flex justify-between items-center py-4">
                    <div class="flex items-center">
                        <div class="text-2xl mr-3">🔬</div>
                        <h1 class="text-gray-900 text-xl font-bold">Тест без pandas</h1>
                    </div>
                    <div class="flex items-center space-x-4">
                        <a href="/" class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded">Дашборд</a>
                        <a href="/ultra-test/" class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded">Ультра</a>
                        <a href="/admin/" class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded">Admin</a>
                    </div>
                </div>
            </div>
        </nav>

        <div class="max-w-4xl mx-auto px-4 py-8">
            <div class="mb-8">
                <h1 class="text-2xl font-bold text-gray-900">Тест без pandas</h1>
                <p class="mt-1 text-sm text-gray-500">Диагностика совместимости версий pandas/openpyxl</p>
            </div>

            <div class="bg-white shadow rounded-lg p-8">
                <div id="upload-area" class="border-2 border-dashed border-gray-300 rounded-lg p-12 text-center hover:border-purple-400 transition-colors cursor-pointer">
                    <div class="mx-auto w-12 h-12 text-gray-400 mb-4">
                        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
                        </svg>
                    </div>
                    <h3 class="text-lg font-medium text-gray-900 mb-2">Перетащите файл сюда</h3>
                    <p class="text-sm text-gray-500 mb-4">или нажмите для выбора файла</p>
                    <input type="file" id="file-input" class="hidden" accept=".csv,.xlsx,.xls">
                    <button onclick="document.getElementById('file-input').click()" class="bg-purple-600 text-white px-4 py-2 rounded-md hover:bg-purple-700">
                        Выбрать файл
                    </button>
                </div>
                
                <div id="result" class="mt-6 hidden">
                    <pre id="result-content" class="bg-gray-100 p-4 rounded-lg overflow-auto max-h-96 text-sm"></pre>
                </div>
            </div>

            <div class="mt-8 bg-white shadow rounded-lg p-6">
                <h3 class="text-lg font-medium text-gray-900 mb-4">Что делает тест без pandas</h3>
                <div class="space-y-3 text-sm text-gray-600">
                    <p>• Сохранение файла</p>
                    <p>• Проверка ZIP структуры (.xlsx это ZIP)</p>
                    <p>• Чтение sharedStrings.xml</p>
                    <p>• Тестирование разных pandas engines</p>
                    <p>• Проверка совместимости версий</p>
                </div>
            </div>
        </div>

        <script>
            const uploadArea = document.getElementById('upload-area');
            const fileInput = document.getElementById('file-input');
            const resultDiv = document.getElementById('result');
            const resultContent = document.getElementById('result-content');

            uploadArea.addEventListener('dragover', (e) => {
                e.preventDefault();
                uploadArea.classList.add('border-purple-400', 'bg-purple-50');
            });

            uploadArea.addEventListener('dragleave', (e) => {
                e.preventDefault();
                uploadArea.classList.remove('border-purple-400', 'bg-purple-50');
            });

            uploadArea.addEventListener('drop', (e) => {
                e.preventDefault();
                uploadArea.classList.remove('border-purple-400', 'bg-purple-50');
                const files = e.dataTransfer.files;
                if (files.length > 0) {
                    handleFileUpload(files[0]);
                }
            });

            fileInput.addEventListener('change', (e) => {
                if (e.target.files.length > 0) {
                    handleFileUpload(e.target.files[0]);
                }
            });

            async function handleFileUpload(file) {
                const formData = new FormData();
                formData.append('file', file);

                resultDiv.classList.remove('hidden');
                resultContent.textContent = 'Тестирование без pandas...';

                try {
                    console.log('Testing file with no-pandas endpoint...');
                    const response = await fetch('/api/upload/no-pandas-test/', {
                        method: 'POST',
                        body: formData
                    });

                    const result = await response.json();
                    console.log('No-pandas test result:', result);

                    resultContent.textContent = JSON.stringify(result, null, 2);
                } catch (error) {
                    resultContent.textContent = 'Ошибка: ' + error.message;
                    console.error('No-pandas test error:', error);
                }
            }
        </script>
    </body>
    </html>
    """
    return HttpResponse(html_content, content_type="text/html")
