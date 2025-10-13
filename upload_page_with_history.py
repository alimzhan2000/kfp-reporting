def get_upload_page_with_history():
    """
    Страница загрузки файлов с историей загрузок
    """
    return """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Загрузка файлов - KFP Reporting</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="https://unpkg.com/lucide@latest/dist/umd/lucide.js"></script>
        <style>
            body {
                font-family: 'Inter', sans-serif;
                background-color: #f3f4f6;
            }
            .upload-area {
                border: 2px dashed #d1d5db;
                transition: all 0.2s ease-in-out;
            }
            .upload-area:hover {
                border-color: #93c5fd;
                background-color: #eff6ff;
            }
            .upload-area.drag-over {
                border-color: #3b82f6;
                background-color: #dbeafe;
            }
            .file-row {
                transition: all 0.2s ease-in-out;
            }
            .file-row:hover {
                background-color: #f9fafb;
            }
            .status-badge {
                font-size: 0.75rem;
                font-weight: 500;
                padding: 0.25rem 0.5rem;
                border-radius: 0.375rem;
            }
            .status-pending {
                background-color: #fef3c7;
                color: #92400e;
            }
            .status-processing {
                background-color: #dbeafe;
                color: #1e40af;
            }
            .status-completed {
                background-color: #d1fae5;
                color: #065f46;
            }
            .status-failed {
                background-color: #fee2e2;
                color: #991b1b;
            }
        </style>
    </head>
    <body>
        <!-- Navigation -->
        <nav class="bg-white shadow-sm border-b">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div class="flex justify-between items-center h-16">
                    <div class="flex items-center space-x-8">
                        <div class="flex items-center space-x-2">
                            <span class="text-2xl">🌾</span>
                            <h1 class="text-xl font-bold text-gray-900">KFP Reporting</h1>
                        </div>
                        <div class="flex items-center space-x-6">
                            <a href="/dashboard/" class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded">Дашборд</a>
                            <a href="/upload/" class="text-blue-600 hover:text-blue-800 px-3 py-2 rounded font-medium">Загрузка</a>
                            <a href="/reports/" class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded">Отчеты</a>
                            <a href="/user-management/" class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded">Admin</a>
                        </div>
                    </div>
                </div>
            </div>
        </nav>

        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <!-- Header -->
            <div class="mb-8">
                <h2 class="text-3xl font-bold text-gray-900">Загрузка файлов</h2>
                <p class="mt-2 text-gray-600">Загрузите CSV или Excel файлы с сельскохозяйственными данными</p>
            </div>

            <!-- Upload Section -->
            <div class="bg-white rounded-lg shadow-sm border p-6 mb-8">
                <h3 class="text-lg font-semibold text-gray-900 mb-4">Загрузить новый файл</h3>
                
                <div id="upload-area" class="upload-area rounded-lg p-8 text-center cursor-pointer">
                    <div class="flex flex-col items-center">
                        <i data-lucide="upload" class="h-12 w-12 text-gray-400 mb-4"></i>
                        <p class="text-lg text-gray-600 mb-2">Перетащите файлы сюда</p>
                        <p class="text-sm text-gray-500 mb-4">или нажмите для выбора файлов</p>
                        <button id="select-files-btn" class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors">
                            Выбрать файлы
                        </button>
                    </div>
                </div>
                
                <input type="file" id="file-input" class="hidden" accept=".csv,.xlsx,.xls">
                
                <!-- Upload Progress -->
                <div id="upload-progress" class="hidden mt-4">
                    <div class="flex items-center space-x-2">
                        <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
                        <span class="text-sm text-gray-600">Загружается...</span>
                    </div>
                </div>
                
                <!-- Upload Result -->
                <div id="upload-result" class="hidden mt-4 p-4 rounded-md"></div>
            </div>

            <!-- Upload History -->
            <div class="bg-white rounded-lg shadow-sm border">
                <div class="p-6 border-b">
                    <div class="flex justify-between items-center">
                        <h3 class="text-lg font-semibold text-gray-900">История загрузок</h3>
                        <button id="refresh-history" class="text-blue-600 hover:text-blue-800 text-sm font-medium">
                            Обновить
                        </button>
                    </div>
                </div>
                
                <div class="overflow-x-auto">
                    <table class="min-w-full divide-y divide-gray-200">
                        <thead class="bg-gray-50">
                            <tr>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                    Файл
                                </th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                    Размер
                                </th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                    Статус
                                </th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                    Записей
                                </th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                    Дата загрузки
                                </th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                    Действия
                                </th>
                            </tr>
                        </thead>
                        <tbody id="upload-history-body" class="bg-white divide-y divide-gray-200">
                            <tr>
                                <td colspan="6" class="px-6 py-4 text-center text-gray-500">
                                    Загрузка истории...
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Instructions -->
            <div class="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-6">
                <h3 class="text-lg font-semibold text-blue-900 mb-4">Инструкции по загрузке</h3>
                <ul class="space-y-2 text-blue-800">
                    <li>• Поддерживаемые форматы: CSV, XLSX, XLS</li>
                    <li>• Файл должен содержать колонки: Поле, Год, Площадь посева, Урожайность, Культура, Сорт, Конечный продукт</li>
                    <li>• Максимальный размер файла: 10 MB</li>
                    <li>• После загрузки данные будут автоматически обработаны и добавлены в систему</li>
                </ul>
            </div>
        </div>

        <script>
            // Initialize Lucide icons
            lucide.createIcons();

            // Upload functionality
            const uploadArea = document.getElementById('upload-area');
            const fileInput = document.getElementById('file-input');
            const selectFilesBtn = document.getElementById('select-files-btn');
            const uploadProgress = document.getElementById('upload-progress');
            const uploadResult = document.getElementById('upload-result');
            const refreshHistoryBtn = document.getElementById('refresh-history');

            // Drag and drop functionality
            uploadArea.addEventListener('dragover', (e) => {
                e.preventDefault();
                uploadArea.classList.add('drag-over');
            });

            uploadArea.addEventListener('dragleave', (e) => {
                e.preventDefault();
                uploadArea.classList.remove('drag-over');
            });

            uploadArea.addEventListener('drop', (e) => {
                e.preventDefault();
                uploadArea.classList.remove('drag-over');
                const files = e.dataTransfer.files;
                if (files.length > 0) {
                    handleFile(files[0]);
                }
            });

            // Click to select files
            selectFilesBtn.addEventListener('click', () => {
                fileInput.click();
            });

            uploadArea.addEventListener('click', () => {
                fileInput.click();
            });

            fileInput.addEventListener('change', (e) => {
                if (e.target.files.length > 0) {
                    handleFile(e.target.files[0]);
                }
            });

            // File upload handler
            async function handleFile(file) {
                // Validate file type
                const allowedTypes = [
                    'text/csv',
                    'application/vnd.ms-excel',
                    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                ];
                
                if (!allowedTypes.includes(file.type) && !file.name.match(/\\.(csv|xlsx|xls)$/i)) {
                    showResult('error', 'Неподдерживаемый формат файла. Разрешены: CSV, XLSX, XLS');
                    return;
                }

                // Validate file size (10MB)
                if (file.size > 10 * 1024 * 1024) {
                    showResult('error', 'Размер файла не должен превышать 10MB');
                    return;
                }

                // Show progress
                uploadProgress.classList.remove('hidden');
                uploadResult.classList.add('hidden');

                try {
                    const formData = new FormData();
                    formData.append('file', file);

                    const response = await fetch('/api/upload/', {
                        method: 'POST',
                        body: formData
                    });

                    const data = await response.json();

                    if (response.ok) {
                        showResult('success', data.message || 'Файл успешно загружен!');
                        // Refresh history
                        loadUploadHistory();
                    } else {
                        showResult('error', data.error || 'Ошибка загрузки файла');
                    }
                } catch (error) {
                    showResult('error', 'Ошибка загрузки файла: ' + error.message);
                } finally {
                    uploadProgress.classList.add('hidden');
                    // Clear file input
                    fileInput.value = '';
                }
            }

            // Show upload result
            function showResult(type, message) {
                uploadResult.classList.remove('hidden');
                uploadResult.className = `mt-4 p-4 rounded-md ${
                    type === 'success' 
                        ? 'bg-green-50 border border-green-200 text-green-800' 
                        : 'bg-red-50 border border-red-200 text-red-800'
                }`;
                uploadResult.textContent = message;
            }

            // Load upload history
            async function loadUploadHistory() {
                const tbody = document.getElementById('upload-history-body');
                
                try {
                    const response = await fetch('/api/upload/history/');
                    const uploads = await response.json();

                    if (uploads.length === 0) {
                        tbody.innerHTML = `
                            <tr>
                                <td colspan="6" class="px-6 py-4 text-center text-gray-500">
                                    Нет загруженных файлов
                                </td>
                            </tr>
                        `;
                        return;
                    }

                    tbody.innerHTML = uploads.map(upload => `
                        <tr class="file-row">
                            <td class="px-6 py-4 whitespace-nowrap">
                                <div class="flex items-center">
                                    <i data-lucide="file" class="h-5 w-5 text-gray-400 mr-3"></i>
                                    <div>
                                        <div class="text-sm font-medium text-gray-900">${upload.file_name}</div>
                                    </div>
                                </div>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                ${formatFileSize(upload.file_size)}
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap">
                                <span class="status-badge status-${upload.status}">
                                    ${getStatusText(upload.status)}
                                </span>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                ${upload.records_created || 0}
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                ${formatDate(upload.created_at)}
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                                <button onclick="deleteUpload(${upload.id})" class="text-red-600 hover:text-red-900">
                                    Удалить
                                </button>
                            </td>
                        </tr>
                    `).join('');

                    // Re-initialize icons
                    lucide.createIcons();
                } catch (error) {
                    tbody.innerHTML = `
                        <tr>
                            <td colspan="6" class="px-6 py-4 text-center text-red-500">
                                Ошибка загрузки истории: ${error.message}
                            </td>
                        </tr>
                    `;
                }
            }

            // Delete upload
            async function deleteUpload(uploadId) {
                if (!confirm('Вы уверены, что хотите удалить этот файл и все его данные?')) {
                    return;
                }

                try {
                    const response = await fetch(`/api/upload/delete/${uploadId}/`, {
                        method: 'DELETE'
                    });

                    const data = await response.json();

                    if (response.ok) {
                        showResult('success', `Файл и данные удалены. Удалено записей: ${data.deleted_records}`);
                        loadUploadHistory();
                    } else {
                        showResult('error', data.error || 'Ошибка удаления файла');
                    }
                } catch (error) {
                    showResult('error', 'Ошибка удаления файла: ' + error.message);
                }
            }

            // Utility functions
            function formatFileSize(bytes) {
                if (bytes === 0) return '0 Bytes';
                const k = 1024;
                const sizes = ['Bytes', 'KB', 'MB', 'GB'];
                const i = Math.floor(Math.log(bytes) / Math.log(k));
                return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
            }

            function formatDate(dateString) {
                const date = new Date(dateString);
                return date.toLocaleString('ru-RU');
            }

            function getStatusText(status) {
                const statusMap = {
                    'pending': 'Ожидает',
                    'processing': 'Обрабатывается',
                    'completed': 'Завершено',
                    'failed': 'Ошибка'
                };
                return statusMap[status] || status;
            }

            // Refresh history button
            refreshHistoryBtn.addEventListener('click', loadUploadHistory);

            // Load history on page load
            loadUploadHistory();
        </script>
    </body>
    </html>
    """
