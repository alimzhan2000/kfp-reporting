from django.http import HttpResponse

@csrf_exempt
def simple_test_page(request):
    """Простая тестовая страница для диагностики файлов"""
    html_content = """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>KFP Reporting - Простой тест</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-50">
        <nav class="bg-white shadow">
            <div class="max-w-7xl mx-auto px-4">
                <div class="flex justify-between items-center py-4">
                    <div class="flex items-center">
                        <div class="text-2xl mr-3">🔬</div>
                        <h1 class="text-gray-900 text-xl font-bold">Простой тест</h1>
                    </div>
                    <div class="flex items-center space-x-4">
                        <a href="/" class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded">Дашборд</a>
                        <a href="/upload-test/" class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded">Тест</a>
                        <a href="/admin/" class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded">Admin</a>
                    </div>
                </div>
            </div>
        </nav>

        <div class="max-w-4xl mx-auto px-4 py-8">
            <div class="mb-8">
                <h1 class="text-2xl font-bold text-gray-900">Простой тест файлов</h1>
                <p class="mt-1 text-sm text-gray-500">Максимально простая диагностика файлов</p>
            </div>

            <div class="bg-white shadow rounded-lg p-8">
                <div id="upload-area" class="border-2 border-dashed border-gray-300 rounded-lg p-12 text-center hover:border-green-400 transition-colors cursor-pointer">
                    <div class="mx-auto w-12 h-12 text-gray-400 mb-4">
                        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
                        </svg>
                    </div>
                    <h3 class="text-lg font-medium text-gray-900 mb-2">Перетащите файл сюда</h3>
                    <p class="text-sm text-gray-500 mb-4">или нажмите для выбора файла</p>
                    <input type="file" id="file-input" class="hidden" accept=".csv,.xlsx,.xls">
                    <button onclick="document.getElementById('file-input').click()" class="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700">
                        Выбрать файл
                    </button>
                </div>
                
                <div id="result" class="mt-6 hidden">
                    <pre id="result-content" class="bg-gray-100 p-4 rounded-lg overflow-auto max-h-96 text-sm"></pre>
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
                uploadArea.classList.add('border-green-400', 'bg-green-50');
            });

            uploadArea.addEventListener('dragleave', (e) => {
                e.preventDefault();
                uploadArea.classList.remove('border-green-400', 'bg-green-50');
            });

            uploadArea.addEventListener('drop', (e) => {
                e.preventDefault();
                uploadArea.classList.remove('border-green-400', 'bg-green-50');
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
                resultContent.textContent = 'Тестирование файла...';

                try {
                    console.log('Testing file with simple endpoint...');
                    const response = await fetch('/api/upload/simple-test/', {
                        method: 'POST',
                        body: formData
                    });

                    const result = await response.json();
                    console.log('Simple test result:', result);

                    resultContent.textContent = JSON.stringify(result, null, 2);
                } catch (error) {
                    resultContent.textContent = 'Ошибка: ' + error.message;
                    console.error('Simple test error:', error);
                }
            }
        </script>
    </body>
    </html>
    """
    return HttpResponse(html_content, content_type="text/html")
