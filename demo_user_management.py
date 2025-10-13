"""
Демо-система управления пользователями (работает с localStorage)
"""
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

# Демо-данные пользователей (в реальном приложении это было бы в базе данных)
DEMO_USERS = [
    {
        'id': 1,
        'username': 'admin',
        'password': 'admin123',
        'role': 'admin',
        'first_name': 'Администратор',
        'last_name': 'Системы',
        'email': 'admin@kfp.com',
        'phone': '+7 (777) 123-45-67',
        'department': 'IT',
        'is_active_user': True,
        'is_active': True,
        'created_at': '2024-01-01T00:00:00Z'
    },
    {
        'id': 2,
        'username': 'manager',
        'password': 'manager123',
        'role': 'manager',
        'first_name': 'Менеджер',
        'last_name': 'Отдела',
        'email': 'manager@kfp.com',
        'phone': '+7 (777) 234-56-78',
        'department': 'Агрономия',
        'is_active_user': True,
        'is_active': True,
        'created_at': '2024-01-02T00:00:00Z'
    },
    {
        'id': 3,
        'username': 'user',
        'password': 'user123',
        'role': 'user',
        'first_name': 'Пользователь',
        'last_name': 'Обычный',
        'email': 'user@kfp.com',
        'phone': '+7 (777) 345-67-89',
        'department': 'Поле',
        'is_active_user': True,
        'is_active': True,
        'created_at': '2024-01-03T00:00:00Z'
    }
]

def get_demo_user_management_page():
    """Возвращает страницу управления пользователями (демо-версия)"""
    return """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Управление пользователями - KFP Reporting</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="https://unpkg.com/lucide@latest/dist/umd/lucide.js"></script>
    </head>
    <body class="bg-gray-50">
        <!-- Header -->
        <nav class="bg-white shadow">
            <div class="max-w-7xl mx-auto px-4">
                <div class="flex justify-between items-center py-4">
                    <div class="flex items-center">
                        <div class="text-2xl mr-3">🌾</div>
                        <h1 class="text-gray-900 text-xl font-bold">KFP Reporting</h1>
                    </div>
                    <div class="flex items-center space-x-4">
                        <a href="/dashboard/" class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded">Дашборд</a>
                        <a href="/upload/" class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded">Загрузка</a>
                        <a href="/reports/" class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded">Отчеты</a>
                        <a href="/admin/" class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded">Admin</a>
                        <div class="flex items-center space-x-2">
                            <span id="user-info" class="text-sm text-gray-600"></span>
                            <button onclick="logout()" class="text-red-600 hover:text-red-800 px-2 py-1 rounded text-sm">
                                Выйти
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </nav>

        <!-- Main Content -->
        <div class="max-w-7xl mx-auto px-4 py-8">
            <div class="mb-8">
                <div class="flex justify-between items-center">
                    <div>
                        <h1 class="text-2xl font-bold text-gray-900">Управление пользователями</h1>
                        <p class="mt-1 text-sm text-gray-500">
                            Создание, редактирование и удаление пользователей системы (Демо-версия)
                        </p>
                        <div class="mt-2 p-3 bg-blue-50 border border-blue-200 rounded-md">
                            <p class="text-sm text-blue-800">
                                <strong>Демо-режим:</strong> Данные сохраняются в localStorage браузера. 
                                В реальной системе они будут храниться в базе данных.
                            </p>
                        </div>
                    </div>
                    <button onclick="openCreateUserModal()" 
                            class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors flex items-center space-x-2">
                        <i data-lucide="plus" class="h-4 w-4"></i>
                        <span>Добавить пользователя</span>
                    </button>
                </div>
            </div>

            <!-- Users Table -->
            <div class="bg-white shadow rounded-lg overflow-hidden">
                <div class="px-6 py-4 border-b border-gray-200">
                    <h3 class="text-lg font-medium text-gray-900">Список пользователей</h3>
                </div>
                
                <div class="overflow-x-auto">
                    <table class="min-w-full divide-y divide-gray-200">
                        <thead class="bg-gray-50">
                            <tr>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                    Пользователь
                                </th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                    Роль
                                </th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                    Контакты
                                </th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                    Статус
                                </th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                    Создан
                                </th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                    Действия
                                </th>
                            </tr>
                        </thead>
                        <tbody id="users-table-body" class="bg-white divide-y divide-gray-200">
                            <tr>
                                <td colspan="6" class="px-6 py-4 text-center text-gray-500">
                                    Загрузка пользователей...
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- Create User Modal -->
        <div id="create-user-modal" class="fixed inset-0 bg-gray-600 bg-opacity-50 hidden z-50">
            <div class="flex items-center justify-center min-h-screen p-4">
                <div class="bg-white rounded-lg shadow-xl max-w-md w-full">
                    <div class="px-6 py-4 border-b border-gray-200">
                        <h3 class="text-lg font-medium text-gray-900">Добавить пользователя</h3>
                    </div>
                    <form id="create-user-form" class="p-6 space-y-4">
                        <div>
                            <label class="block text-sm font-medium text-gray-700">Имя пользователя *</label>
                            <input type="text" id="create-username" required
                                   class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500">
                        </div>
                        
                        <div>
                            <label class="block text-sm font-medium text-gray-700">Пароль *</label>
                            <input type="password" id="create-password" required
                                   class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500">
                        </div>
                        
                        <div>
                            <label class="block text-sm font-medium text-gray-700">Роль *</label>
                            <select id="create-role" required
                                    class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500">
                                <option value="">Выберите роль</option>
                                <option value="admin">Администратор</option>
                                <option value="manager">Менеджер</option>
                                <option value="user">Пользователь</option>
                            </select>
                        </div>
                        
                        <div class="grid grid-cols-2 gap-4">
                            <div>
                                <label class="block text-sm font-medium text-gray-700">Имя</label>
                                <input type="text" id="create-first-name"
                                       class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500">
                            </div>
                            <div>
                                <label class="block text-sm font-medium text-gray-700">Фамилия</label>
                                <input type="text" id="create-last-name"
                                       class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500">
                            </div>
                        </div>
                        
                        <div>
                            <label class="block text-sm font-medium text-gray-700">Email</label>
                            <input type="email" id="create-email"
                                   class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500">
                        </div>
                        
                        <div>
                            <label class="block text-sm font-medium text-gray-700">Телефон</label>
                            <input type="tel" id="create-phone"
                                   class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500">
                        </div>
                        
                        <div>
                            <label class="block text-sm font-medium text-gray-700">Отдел</label>
                            <input type="text" id="create-department"
                                   class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500">
                        </div>
                        
                        <div class="flex items-center">
                            <input type="checkbox" id="create-is-active" checked
                                   class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded">
                            <label class="ml-2 block text-sm text-gray-900">Активный пользователь</label>
                        </div>
                    </form>
                    <div class="px-6 py-4 border-t border-gray-200 flex justify-end space-x-3">
                        <button onclick="closeCreateUserModal()"
                                class="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50">
                            Отмена
                        </button>
                        <button onclick="createUser()"
                                class="px-4 py-2 bg-blue-600 text-white rounded-md text-sm font-medium hover:bg-blue-700">
                            Создать
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Edit User Modal -->
        <div id="edit-user-modal" class="fixed inset-0 bg-gray-600 bg-opacity-50 hidden z-50">
            <div class="flex items-center justify-center min-h-screen p-4">
                <div class="bg-white rounded-lg shadow-xl max-w-md w-full">
                    <div class="px-6 py-4 border-b border-gray-200">
                        <h3 class="text-lg font-medium text-gray-900">Редактировать пользователя</h3>
                    </div>
                    <form id="edit-user-form" class="p-6 space-y-4">
                        <input type="hidden" id="edit-user-id">
                        
                        <div>
                            <label class="block text-sm font-medium text-gray-700">Имя пользователя *</label>
                            <input type="text" id="edit-username" required
                                   class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500">
                        </div>
                        
                        <div>
                            <label class="block text-sm font-medium text-gray-700">Новый пароль (оставьте пустым, чтобы не менять)</label>
                            <input type="password" id="edit-password"
                                   class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500">
                        </div>
                        
                        <div>
                            <label class="block text-sm font-medium text-gray-700">Роль *</label>
                            <select id="edit-role" required
                                    class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500">
                                <option value="">Выберите роль</option>
                                <option value="admin">Администратор</option>
                                <option value="manager">Менеджер</option>
                                <option value="user">Пользователь</option>
                            </select>
                        </div>
                        
                        <div class="grid grid-cols-2 gap-4">
                            <div>
                                <label class="block text-sm font-medium text-gray-700">Имя</label>
                                <input type="text" id="edit-first-name"
                                       class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500">
                            </div>
                            <div>
                                <label class="block text-sm font-medium text-gray-700">Фамилия</label>
                                <input type="text" id="edit-last-name"
                                       class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500">
                            </div>
                        </div>
                        
                        <div>
                            <label class="block text-sm font-medium text-gray-700">Email</label>
                            <input type="email" id="edit-email"
                                   class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500">
                        </div>
                        
                        <div>
                            <label class="block text-sm font-medium text-gray-700">Телефон</label>
                            <input type="tel" id="edit-phone"
                                   class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500">
                        </div>
                        
                        <div>
                            <label class="block text-sm font-medium text-gray-700">Отдел</label>
                            <input type="text" id="edit-department"
                                   class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500">
                        </div>
                        
                        <div class="flex items-center space-x-4">
                            <div class="flex items-center">
                                <input type="checkbox" id="edit-is-active"
                                       class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded">
                                <label class="ml-2 block text-sm text-gray-900">Активный</label>
                            </div>
                            <div class="flex items-center">
                                <input type="checkbox" id="edit-is-active-user"
                                       class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded">
                                <label class="ml-2 block text-sm text-gray-900">Активный пользователь</label>
                            </div>
                        </div>
                    </form>
                    <div class="px-6 py-4 border-t border-gray-200 flex justify-end space-x-3">
                        <button onclick="closeEditUserModal()"
                                class="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50">
                            Отмена
                        </button>
                        <button onclick="updateUser()"
                                class="px-4 py-2 bg-green-600 text-white rounded-md text-sm font-medium hover:bg-green-700">
                            Сохранить
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Success/Error Messages -->
        <div id="message-container" class="fixed top-4 right-4 z-50"></div>

        <script>
            // Initialize Lucide icons
            lucide.createIcons();

            let currentUsers = [];
            let nextUserId = 4; // Начинаем с 4, так как у нас уже есть 3 демо-пользователя

            // Check authentication
            function checkAuth() {
                const userData = localStorage.getItem('kfp_user');
                if (!userData) {
                    window.location.href = '/login/';
                    return null;
                }
                
                const user = JSON.parse(userData);
                if (user.role !== 'admin') {
                    alert('У вас нет прав доступа к управлению пользователями');
                    window.location.href = '/dashboard/';
                    return null;
                }
                
                document.getElementById('user-info').textContent = `${user.username} (${user.role})`;
                return user;
            }

            // Logout function
            function logout() {
                localStorage.removeItem('kfp_user');
                window.location.href = '/login/';
            }

            // Load users from localStorage
            function loadUsers() {
                const storedUsers = localStorage.getItem('kfp_demo_users');
                if (storedUsers) {
                    currentUsers = JSON.parse(storedUsers);
                } else {
                    // Инициализируем с демо-данными
                    currentUsers = JSON.parse(`""" + json.dumps(DEMO_USERS, ensure_ascii=False) + """`);
                    localStorage.setItem('kfp_demo_users', JSON.stringify(currentUsers));
                }
                
                // Находим максимальный ID для nextUserId
                const maxId = Math.max(...currentUsers.map(u => u.id));
                nextUserId = maxId + 1;
                
                renderUsersTable(currentUsers);
            }

            // Save users to localStorage
            function saveUsers() {
                localStorage.setItem('kfp_demo_users', JSON.stringify(currentUsers));
            }

            // Render users table
            function renderUsersTable(users) {
                const tbody = document.getElementById('users-table-body');
                
                if (users.length === 0) {
                    tbody.innerHTML = `
                        <tr>
                            <td colspan="6" class="px-6 py-4 text-center text-gray-500">
                                Пользователи не найдены
                            </td>
                        </tr>
                    `;
                    return;
                }
                
                tbody.innerHTML = users.map(user => `
                    <tr>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <div class="flex items-center">
                                <div class="flex-shrink-0 h-10 w-10">
                                    <div class="h-10 w-10 rounded-full bg-gray-300 flex items-center justify-center">
                                        <span class="text-sm font-medium text-gray-700">
                                            ${(user.first_name + ' ' + user.last_name).trim().charAt(0).toUpperCase() || user.username.charAt(0).toUpperCase()}
                                        </span>
                                    </div>
                                </div>
                                <div class="ml-4">
                                    <div class="text-sm font-medium text-gray-900">${(user.first_name + ' ' + user.last_name).trim() || user.username}</div>
                                    <div class="text-sm text-gray-500">@${user.username}</div>
                                </div>
                            </div>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                                user.role === 'admin' ? 'bg-red-100 text-red-800' :
                                user.role === 'manager' ? 'bg-blue-100 text-blue-800' :
                                'bg-green-100 text-green-800'
                            }">
                                ${user.role === 'admin' ? 'Администратор' : user.role === 'manager' ? 'Менеджер' : 'Пользователь'}
                            </span>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            <div>${user.email || '-'}</div>
                            <div>${user.phone || '-'}</div>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <div class="flex items-center space-x-2">
                                <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                                    user.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                                }">
                                    ${user.is_active ? 'Активен' : 'Неактивен'}
                                </span>
                                ${user.is_active_user ? '<span class="text-green-600">✓</span>' : '<span class="text-red-600">✗</span>'}
                            </div>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            ${new Date(user.created_at).toLocaleDateString('ru-RU')}
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                            <div class="flex space-x-2">
                                <button onclick="editUser(${user.id})" 
                                        class="text-blue-600 hover:text-blue-900">Редактировать</button>
                                <button onclick="deleteUser(${user.id})" 
                                        class="text-red-600 hover:text-red-900">Удалить</button>
                            </div>
                        </td>
                    </tr>
                `).join('');
            }

            // Create user modal functions
            function openCreateUserModal() {
                document.getElementById('create-user-modal').classList.remove('hidden');
                document.getElementById('create-user-form').reset();
            }

            function closeCreateUserModal() {
                document.getElementById('create-user-modal').classList.add('hidden');
            }

            // Create user
            function createUser() {
                const newUser = {
                    id: nextUserId++,
                    username: document.getElementById('create-username').value,
                    password: document.getElementById('create-password').value,
                    role: document.getElementById('create-role').value,
                    first_name: document.getElementById('create-first-name').value,
                    last_name: document.getElementById('create-last-name').value,
                    email: document.getElementById('create-email').value,
                    phone: document.getElementById('create-phone').value,
                    department: document.getElementById('create-department').value,
                    is_active_user: document.getElementById('create-is-active').checked,
                    is_active: true,
                    created_at: new Date().toISOString()
                };
                
                // Проверка на дублирование username
                if (currentUsers.find(u => u.username === newUser.username)) {
                    showMessage('Пользователь с таким именем уже существует', 'error');
                    return;
                }
                
                currentUsers.push(newUser);
                saveUsers();
                showMessage(`Пользователь ${newUser.username} успешно создан`, 'success');
                closeCreateUserModal();
                loadUsers();
            }

            // Edit user modal functions
            function editUser(userId) {
                const user = currentUsers.find(u => u.id === userId);
                if (!user) return;
                
                document.getElementById('edit-user-id').value = user.id;
                document.getElementById('edit-username').value = user.username;
                document.getElementById('edit-role').value = user.role;
                document.getElementById('edit-first-name').value = user.first_name || '';
                document.getElementById('edit-last-name').value = user.last_name || '';
                document.getElementById('edit-email').value = user.email || '';
                document.getElementById('edit-phone').value = user.phone || '';
                document.getElementById('edit-department').value = user.department || '';
                document.getElementById('edit-is-active').checked = user.is_active;
                document.getElementById('edit-is-active-user').checked = user.is_active_user;
                
                document.getElementById('edit-user-modal').classList.remove('hidden');
            }

            function closeEditUserModal() {
                document.getElementById('edit-user-modal').classList.add('hidden');
            }

            // Update user
            function updateUser() {
                const userId = parseInt(document.getElementById('edit-user-id').value);
                const userIndex = currentUsers.findIndex(u => u.id === userId);
                
                if (userIndex === -1) {
                    showMessage('Пользователь не найден', 'error');
                    return;
                }
                
                const user = currentUsers[userIndex];
                const newUsername = document.getElementById('edit-username').value;
                
                // Проверка на дублирование username (кроме текущего пользователя)
                if (newUsername !== user.username && currentUsers.find(u => u.username === newUsername)) {
                    showMessage('Пользователь с таким именем уже существует', 'error');
                    return;
                }
                
                // Обновляем данные
                user.username = newUsername;
                user.role = document.getElementById('edit-role').value;
                user.first_name = document.getElementById('edit-first-name').value;
                user.last_name = document.getElementById('edit-last-name').value;
                user.email = document.getElementById('edit-email').value;
                user.phone = document.getElementById('edit-phone').value;
                user.department = document.getElementById('edit-department').value;
                user.is_active = document.getElementById('edit-is-active').checked;
                user.is_active_user = document.getElementById('edit-is-active-user').checked;
                
                const password = document.getElementById('edit-password').value;
                if (password) {
                    user.password = password;
                }
                
                currentUsers[userIndex] = user;
                saveUsers();
                showMessage(`Пользователь ${user.username} успешно обновлен`, 'success');
                closeEditUserModal();
                loadUsers();
            }

            // Delete user
            function deleteUser(userId) {
                if (!confirm('Вы уверены, что хотите удалить этого пользователя?')) {
                    return;
                }
                
                const userIndex = currentUsers.findIndex(u => u.id === userId);
                if (userIndex === -1) {
                    showMessage('Пользователь не найден', 'error');
                    return;
                }
                
                const user = currentUsers[userIndex];
                currentUsers.splice(userIndex, 1);
                saveUsers();
                showMessage(`Пользователь ${user.username} успешно удален`, 'success');
                loadUsers();
            }

            // Show message
            function showMessage(message, type) {
                const container = document.getElementById('message-container');
                const messageDiv = document.createElement('div');
                
                messageDiv.className = `mb-4 p-4 rounded-md ${
                    type === 'success' ? 'bg-green-50 border border-green-200 text-green-800' :
                    type === 'error' ? 'bg-red-50 border border-red-200 text-red-800' :
                    'bg-blue-50 border border-blue-200 text-blue-800'
                }`;
                
                messageDiv.innerHTML = `
                    <div class="flex justify-between items-center">
                        <span>${message}</span>
                        <button onclick="this.parentElement.parentElement.remove()" 
                                class="ml-4 text-gray-400 hover:text-gray-600">
                            <i data-lucide="x" class="h-4 w-4"></i>
                        </button>
                    </div>
                `;
                
                container.appendChild(messageDiv);
                lucide.createIcons();
                
                setTimeout(() => {
                    if (messageDiv.parentElement) {
                        messageDiv.remove();
                    }
                }, 5000);
            }

            // Initialize page
            const user = checkAuth();
            if (user) {
                loadUsers();
            }
        </script>
    </body>
    </html>
    """

@csrf_exempt
@require_http_methods(["GET"])
def demo_list_users(request):
    """API для получения списка пользователей (демо)"""
    try:
        # В реальном приложении здесь был бы запрос к базе данных
        # Для демо возвращаем фиксированные данные
        return JsonResponse({
            'success': True,
            'users': DEMO_USERS,
            'total': len(DEMO_USERS),
            'message': 'Демо-данные пользователей'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': 'Ошибка получения списка пользователей'
        }, status=500)
