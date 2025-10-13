"""
Система управления пользователями с базой данных для KFP Reporting
"""
from django.http import HttpResponse

def get_database_user_management_page():
    """Возвращает страницу управления пользователями с базой данных"""
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
                            Создание, редактирование и удаление пользователей системы
                        </p>
                        <div class="mt-2 p-3 bg-green-50 border border-green-200 rounded-md">
                            <p class="text-sm text-green-800">
                                <strong>База данных:</strong> Все данные сохраняются в PostgreSQL. 
                                Изменения сохраняются навсегда.
                            </p>
                        </div>
                    </div>
                    <div class="flex space-x-3">
                        <button onclick="initializeDemoUsers()" 
                                class="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 transition-colors flex items-center space-x-2">
                            <i data-lucide="database" class="h-4 w-4"></i>
                            <span>Инициализировать демо</span>
                        </button>
                        <button onclick="openCreateUserModal()" 
                                class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors flex items-center space-x-2">
                            <i data-lucide="plus" class="h-4 w-4"></i>
                            <span>Добавить пользователя</span>
                        </button>
                    </div>
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

            // Load users from database via API
            async function loadUsers() {
                try {
                    const response = await fetch('/api/auth/users/');
                    const data = await response.json();
                    
                    if (data.success) {
                        currentUsers = data.users;
                        renderUsersTable(data.users);
                    } else {
                        showMessage('Ошибка загрузки пользователей: ' + data.error, 'error');
                    }
                } catch (error) {
                    console.error('Error loading users:', error);
                    showMessage('Ошибка загрузки пользователей', 'error');
                }
            }

            // Initialize demo users
            async function initializeDemoUsers() {
                if (!confirm('Инициализировать демо-пользователей в базе данных? Это создаст admin, manager и user.')) {
                    return;
                }
                
                try {
                    const response = await fetch('/api/auth/users/initialize-demo/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        }
                    });
                    
                    const data = await response.json();
                    
                    if (data.success) {
                        showMessage(data.message, 'success');
                        loadUsers(); // Перезагружаем список пользователей
                    } else {
                        showMessage('Ошибка инициализации: ' + data.error, 'error');
                    }
                } catch (error) {
                    console.error('Error initializing demo users:', error);
                    showMessage('Ошибка инициализации демо-пользователей', 'error');
                }
            }

            // Render users table
            function renderUsersTable(users) {
                const tbody = document.getElementById('users-table-body');
                
                if (users.length === 0) {
                    tbody.innerHTML = `
                        <tr>
                            <td colspan="6" class="px-6 py-4 text-center text-gray-500">
                                Пользователи не найдены. Нажмите "Инициализировать демо" для создания демо-пользователей.
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
                                            ${(user.full_name || user.username).charAt(0).toUpperCase()}
                                        </span>
                                    </div>
                                </div>
                                <div class="ml-4">
                                    <div class="text-sm font-medium text-gray-900">${user.full_name || user.username}</div>
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
                                ${user.role_display}
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
            async function createUser() {
                const formData = {
                    username: document.getElementById('create-username').value,
                    password: document.getElementById('create-password').value,
                    role: document.getElementById('create-role').value,
                    first_name: document.getElementById('create-first-name').value,
                    last_name: document.getElementById('create-last-name').value,
                    email: document.getElementById('create-email').value,
                    phone: document.getElementById('create-phone').value,
                    department: document.getElementById('create-department').value,
                    is_active_user: document.getElementById('create-is-active').checked
                };
                
                try {
                    const response = await fetch('/api/auth/users/create/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(formData)
                    });
                    
                    const data = await response.json();
                    
                    if (data.success) {
                        showMessage(data.message, 'success');
                        closeCreateUserModal();
                        loadUsers();
                    } else {
                        showMessage('Ошибка создания пользователя: ' + data.error, 'error');
                    }
                } catch (error) {
                    console.error('Error creating user:', error);
                    showMessage('Ошибка создания пользователя', 'error');
                }
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
            async function updateUser() {
                const userId = document.getElementById('edit-user-id').value;
                const formData = {
                    username: document.getElementById('edit-username').value,
                    role: document.getElementById('edit-role').value,
                    first_name: document.getElementById('edit-first-name').value,
                    last_name: document.getElementById('edit-last-name').value,
                    email: document.getElementById('edit-email').value,
                    phone: document.getElementById('edit-phone').value,
                    department: document.getElementById('edit-department').value,
                    is_active: document.getElementById('edit-is-active').checked,
                    is_active_user: document.getElementById('edit-is-active-user').checked
                };
                
                const password = document.getElementById('edit-password').value;
                if (password) {
                    formData.password = password;
                }
                
                try {
                    const response = await fetch(`/api/auth/users/${userId}/update/`, {
                        method: 'PUT',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(formData)
                    });
                    
                    const data = await response.json();
                    
                    if (data.success) {
                        showMessage(data.message, 'success');
                        closeEditUserModal();
                        loadUsers();
                    } else {
                        showMessage('Ошибка обновления пользователя: ' + data.error, 'error');
                    }
                } catch (error) {
                    console.error('Error updating user:', error);
                    showMessage('Ошибка обновления пользователя', 'error');
                }
            }

            // Delete user
            async function deleteUser(userId) {
                if (!confirm('Вы уверены, что хотите удалить этого пользователя?')) {
                    return;
                }
                
                try {
                    const response = await fetch(`/api/auth/users/${userId}/delete/`, {
                        method: 'DELETE'
                    });
                    
                    const data = await response.json();
                    
                    if (data.success) {
                        showMessage(data.message, 'success');
                        loadUsers();
                    } else {
                        showMessage('Ошибка удаления пользователя: ' + data.error, 'error');
                    }
                } catch (error) {
                    console.error('Error deleting user:', error);
                    showMessage('Ошибка удаления пользователя', 'error');
                }
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
