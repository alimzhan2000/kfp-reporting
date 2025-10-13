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

        <!-- Create User Modal -->
        <div id="create-user-modal" class="hidden fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
            <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
                <div class="mt-3">
                    <h3 class="text-lg font-medium text-gray-900 mb-4">Добавить пользователя</h3>
                    <form id="create-user-form">
                        <div class="mb-4">
                            <label class="block text-sm font-medium text-gray-700 mb-2">Имя пользователя</label>
                            <input type="text" name="username" required 
                                   class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                        </div>
                        <div class="mb-4">
                            <label class="block text-sm font-medium text-gray-700 mb-2">Пароль</label>
                            <input type="password" name="password" required 
                                   class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                        </div>
                        <div class="mb-4">
                            <label class="block text-sm font-medium text-gray-700 mb-2">Роль</label>
                            <select name="role" required 
                                    class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                                <option value="user">Пользователь</option>
                                <option value="manager">Менеджер</option>
                                <option value="admin">Администратор</option>
                            </select>
                        </div>
                        <div class="mb-4">
                            <label class="block text-sm font-medium text-gray-700 mb-2">Email</label>
                            <input type="email" name="email" 
                                   class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                        </div>
                        <div class="flex justify-end space-x-3">
                            <button type="button" onclick="closeCreateUserModal()" 
                                    class="px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400">
                                Отмена
                            </button>
                            <button type="submit" 
                                    class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">
                                Создать
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>

        <script>
            // Simple functions - defined first
            function testFunction() {
                alert('Тестовая функция работает!');
            }
            
            function openCreateUserModal() {
                document.getElementById('create-user-modal').classList.remove('hidden');
            }
            
            function closeCreateUserModal() {
                document.getElementById('create-user-modal').classList.add('hidden');
            }
            
            function loadUsers() {
                alert('Загрузка пользователей запущена!');
            }
            
            // Handle form submission
            document.getElementById('create-user-form').addEventListener('submit', function(e) {
                e.preventDefault();
                const formData = new FormData(this);
                const userData = {
                    username: formData.get('username'),
                    password: formData.get('password'),
                    role: formData.get('role'),
                    email: formData.get('email')
                };
                alert('Пользователь будет создан: ' + JSON.stringify(userData, null, 2));
                closeCreateUserModal();
            });
            
            // Initialize page
            console.log('Simple user management page loaded');
        </script>
    </body>
    </html>
    """
