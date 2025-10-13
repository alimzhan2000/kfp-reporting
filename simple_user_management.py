def get_simple_user_management_page():
    return """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Управление пользователями - Простая версия</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-50">
        <div class="min-h-screen">
            <!-- Header -->
            <div class="bg-white shadow">
                <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div class="flex justify-between items-center py-6">
                        <div>
                            <h1 class="text-3xl font-bold text-gray-900">Управление пользователями</h1>
                            <p class="text-gray-600">Простая версия для тестирования</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Main Content -->
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <!-- Buttons -->
                <div class="bg-white rounded-lg shadow p-6 mb-8">
                    <h2 class="text-lg font-medium text-gray-900 mb-4">Тестирование кнопок</h2>
                    <div class="flex space-x-3">
                        <button onclick="alert('Простой alert работает!')" 
                                class="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700">
                            ✅ Простой alert
                        </button>
                        <button onclick="testFunction()" 
                                class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700">
                            🔧 Тест функции
                        </button>
                        <button onclick="openCreateUserModal()" 
                                class="bg-purple-600 text-white px-4 py-2 rounded-md hover:bg-purple-700">
                            👤 Добавить пользователя
                        </button>
                        <button onclick="loadUsers()" 
                                class="bg-orange-600 text-white px-4 py-2 rounded-md hover:bg-orange-700">
                            📋 Загрузить пользователей
                        </button>
                    </div>
                </div>

                <!-- Users Table -->
                <div class="bg-white rounded-lg shadow">
                    <div class="px-6 py-4 border-b border-gray-200">
                        <h3 class="text-lg font-medium text-gray-900">Список пользователей</h3>
                    </div>
                    <div class="overflow-x-auto">
                        <table class="min-w-full divide-y divide-gray-200">
                            <thead class="bg-gray-50">
                                <tr>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Пользователь</th>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Роль</th>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Статус</th>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Действия</th>
                                </tr>
                            </thead>
                            <tbody id="users-table-body">
                                <tr>
                                    <td colspan="4" class="px-6 py-4 text-center text-gray-500">
                                        Загрузка пользователей...
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>

        <script>
            // Simple functions - defined first
            function testFunction() {
                alert('Тестовая функция работает!');
            }
            
            function openCreateUserModal() {
                alert('Модальное окно для добавления пользователя будет открыто!');
            }
            
            function loadUsers() {
                alert('Загрузка пользователей запущена!');
            }
            
            // Initialize page
            console.log('Simple user management page loaded');
        </script>
    </body>
    </html>
    """
