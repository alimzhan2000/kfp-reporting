def get_improved_user_management_page():
    return """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Управление пользователями - Reporting KFP</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="https://unpkg.com/lucide@latest/dist/umd/lucide.js"></script>
    </head>
    <body class="bg-gray-50">
        <div class="min-h-screen">
            <!-- Header -->
            <nav class="bg-white shadow">
                <div class="max-w-7xl mx-auto px-4">
                    <div class="flex justify-between items-center py-4">
                        <div class="flex items-center">
                            <div class="text-2xl mr-3">🌾</div>
                            <h1 class="text-gray-900 text-xl font-bold">Reporting KFP</h1>
                        </div>
                        <div class="flex items-center space-x-4">
                            <a href="/dashboard/" class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded">Дашборд</a>
                            <a href="/reports/yield-comparison/" class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded">Отчеты</a>
                            <a href="/user-management/" class="text-blue-600 hover:text-blue-800 px-3 py-2 rounded font-medium">Пользователи</a>
                            <a href="/admin/" class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded">Admin</a>
                            <div class="flex items-center space-x-2">
                                <button onclick="goToDashboard()" class="text-blue-600 hover:text-blue-800 px-2 py-1 rounded text-sm">
                                    ← Назад к дашборду
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
                                Создание и управление пользователями системы
                            </p>
                        </div>
                        <div class="flex space-x-3">
                            <button onclick="loadUsers()" 
                                    class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 flex items-center">
                                <i data-lucide="refresh-cw" class="w-4 h-4 mr-2"></i>
                                Обновить список
                            </button>
                            <button onclick="openCreateUserModal()" 
                                    class="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 flex items-center">
                                <i data-lucide="user-plus" class="w-4 h-4 mr-2"></i>
                                Добавить пользователя
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Users List -->
                <div class="bg-white rounded-lg shadow">
                    <div class="px-6 py-4 border-b border-gray-200">
                        <h2 class="text-lg font-medium text-gray-900">Список пользователей</h2>
                    </div>
                    <div id="users-list" class="p-6">
                        <div class="text-center text-gray-500">
                            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-2"></div>
                            Загрузка пользователей...
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Create User Modal -->
        <div id="create-user-modal" class="hidden fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
            <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
                <div class="mt-3">
                    <div class="flex items-center justify-between mb-4">
                        <h3 class="text-lg font-medium text-gray-900">Создать пользователя</h3>
                        <button onclick="closeCreateUserModal()" class="text-gray-400 hover:text-gray-600">
                            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                            </svg>
                        </button>
                    </div>
                    <form id="create-user-form">
                        <div class="mb-4">
                            <label class="block text-sm font-medium text-gray-700 mb-2">Имя пользователя *</label>
                            <input type="text" name="username" required 
                                   class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                        </div>
                        <div class="mb-4">
                            <label class="block text-sm font-medium text-gray-700 mb-2">Пароль *</label>
                            <input type="password" name="password" required 
                                   class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                        </div>
                        <div class="mb-4">
                            <label class="block text-sm font-medium text-gray-700 mb-2">Имя</label>
                            <input type="text" name="first_name" 
                                   class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                        </div>
                        <div class="mb-4">
                            <label class="block text-sm font-medium text-gray-700 mb-2">Фамилия</label>
                            <input type="text" name="last_name" 
                                   class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                        </div>
                        <div class="mb-4">
                            <label class="block text-sm font-medium text-gray-700 mb-2">Роль *</label>
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
                        <div class="mb-4">
                            <label class="block text-sm font-medium text-gray-700 mb-2">Телефон</label>
                            <input type="text" name="phone" 
                                   class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                        </div>
                        <div class="mb-4">
                            <label class="block text-sm font-medium text-gray-700 mb-2">Отдел</label>
                            <input type="text" name="department" 
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

        <!-- Edit User Modal -->
        <div id="edit-user-modal" class="hidden fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
            <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
                <div class="mt-3">
                    <div class="flex items-center justify-between mb-4">
                        <h3 class="text-lg font-medium text-gray-900">Редактировать пользователя</h3>
                        <button onclick="closeEditUserModal()" class="text-gray-400 hover:text-gray-600">
                            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                            </svg>
                        </button>
                    </div>
                    <form id="edit-user-form">
                        <input type="hidden" id="edit-user-id" name="user_id">
                        <div class="mb-4">
                            <label class="block text-sm font-medium text-gray-700 mb-2">Имя пользователя *</label>
                            <input type="text" id="edit-username" name="username" required 
                                   class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                        </div>
                        <div class="mb-4">
                            <label class="block text-sm font-medium text-gray-700 mb-2">Имя</label>
                            <input type="text" id="edit-first-name" name="first_name" 
                                   class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                        </div>
                        <div class="mb-4">
                            <label class="block text-sm font-medium text-gray-700 mb-2">Фамилия</label>
                            <input type="text" id="edit-last-name" name="last_name" 
                                   class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                        </div>
                        <div class="mb-4">
                            <label class="block text-sm font-medium text-gray-700 mb-2">Роль *</label>
                            <select id="edit-role" name="role" required 
                                    class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                                <option value="user">Пользователь</option>
                                <option value="manager">Менеджер</option>
                                <option value="admin">Администратор</option>
                            </select>
                        </div>
                        <div class="mb-4">
                            <label class="block text-sm font-medium text-gray-700 mb-2">Email</label>
                            <input type="email" id="edit-email" name="email" 
                                   class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                        </div>
                        <div class="mb-4">
                            <label class="block text-sm font-medium text-gray-700 mb-2">Отдел</label>
                            <input type="text" id="edit-department" name="department" 
                                   class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                        </div>
                        <div class="flex justify-end space-x-3">
                            <button type="button" onclick="closeEditUserModal()" 
                                    class="px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400">
                                Отмена
                            </button>
                            <button type="submit" 
                                    class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">
                                Сохранить
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>

        <script>
            // Load users on page load
            document.addEventListener('DOMContentLoaded', function() {
                loadUsers();
                // Initialize Lucide icons
                if (typeof lucide !== 'undefined') {
                    lucide.createIcons();
                }
            });
            
            function goToDashboard() {
                window.location.href = '/dashboard/';
            }

            function openCreateUserModal() {
                document.getElementById('create-user-modal').classList.remove('hidden');
            }
            
            function closeCreateUserModal() {
                document.getElementById('create-user-modal').classList.add('hidden');
                document.getElementById('create-user-form').reset();
            }
            
            function closeEditUserModal() {
                document.getElementById('edit-user-modal').classList.add('hidden');
                document.getElementById('edit-user-form').reset();
            }
            
            function loadUsers() {
                const usersList = document.getElementById('users-list');
                usersList.innerHTML = `
                    <div class="text-center text-gray-500">
                        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-2"></div>
                        Загрузка пользователей...
                    </div>
                `;
                
                fetch('/api/reports/simple-users-list/')
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        displayUsers(data.users);
                    } else {
                        usersList.innerHTML = `
                            <div class="text-center text-red-600">
                                <p>Ошибка загрузки пользователей: ${data.error}</p>
                                <button onclick="loadUsers()" class="mt-2 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">
                                    Попробовать снова
                                </button>
                            </div>
                        `;
                    }
                })
                .catch(error => {
                    usersList.innerHTML = `
                        <div class="text-center text-red-600">
                            <p>Ошибка соединения: ${error.message}</p>
                            <button onclick="loadUsers()" class="mt-2 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">
                                Попробовать снова
                            </button>
                        </div>
                    `;
                });
            }
            
            function displayUsers(users) {
                const usersList = document.getElementById('users-list');
                
                if (users.length === 0) {
                    usersList.innerHTML = `
                        <div class="text-center text-gray-500">
                            <p>Пользователи не найдены</p>
                            <button onclick="openCreateUserModal()" class="mt-2 px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700">
                                Создать первого пользователя
                            </button>
                        </div>
                    `;
                    return;
                }
                
                let html = `
                    <div class="overflow-x-auto">
                        <table class="min-w-full divide-y divide-gray-200">
                            <thead class="bg-gray-50">
                                <tr>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Пользователь</th>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Роль</th>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Email</th>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Отдел</th>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Статус</th>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Действия</th>
                                </tr>
                            </thead>
                            <tbody class="bg-white divide-y divide-gray-200">
                `;
                
                users.forEach(user => {
                    const statusColor = user.is_active ? 'text-green-600' : 'text-red-600';
                    const statusText = user.is_active ? 'Активен' : 'Неактивен';
                    const roleColor = user.role === 'admin' ? 'bg-red-100 text-red-800' : 
                                   user.role === 'manager' ? 'bg-blue-100 text-blue-800' : 
                                   'bg-gray-100 text-gray-800';
                    
                    html += `
                        <tr data-user-id="${user.id}">
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${user.id}</td>
                            <td class="px-6 py-4 whitespace-nowrap">
                                <div class="text-sm font-medium text-gray-900">${user.username}</div>
                                <div class="text-sm text-gray-500">${user.first_name} ${user.last_name}</div>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap">
                                <span class="inline-flex px-2 py-1 text-xs font-semibold rounded-full ${roleColor}">
                                    ${user.role}
                                </span>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${user.email || '-'}</td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${user.department || '-'}</td>
                            <td class="px-6 py-4 whitespace-nowrap">
                                <span class="text-sm ${statusColor}">${statusText}</span>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                                <div class="flex space-x-2">
                                    <button onclick="editUser(${user.id})" 
                                            class="text-blue-600 hover:text-blue-900 px-2 py-1 rounded hover:bg-blue-50 flex items-center">
                                        <i data-lucide="edit" class="w-4 h-4 mr-1"></i>
                                        Редактировать
                                    </button>
                                    <button onclick="deleteUser(${user.id})" 
                                            class="text-red-600 hover:text-red-900 px-2 py-1 rounded hover:bg-red-50 flex items-center">
                                        <i data-lucide="trash-2" class="w-4 h-4 mr-1"></i>
                                        Удалить
                                    </button>
                                </div>
                            </td>
                        </tr>
                    `;
                });
                
                html += `
                            </tbody>
                        </table>
                    </div>
                `;
                
                usersList.innerHTML = html;
                
                // Reinitialize Lucide icons after DOM update
                if (typeof lucide !== 'undefined') {
                    lucide.createIcons();
                }
            }
            
            // Handle form submission
            document.getElementById('create-user-form').addEventListener('submit', function(e) {
                e.preventDefault();
                
                const formData = new FormData(this);
                const data = Object.fromEntries(formData.entries());
                
                // Show loading state
                const submitButton = this.querySelector('button[type="submit"]');
                const originalText = submitButton.textContent;
                submitButton.textContent = 'Создание...';
                submitButton.disabled = true;
                
                fetch('/api/reports/simple-create-user/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify(data)
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Show success message
                        alert(`✅ ${data.message}`);
                        
                        // Close modal
                        closeCreateUserModal();
                        
                        // Reload users list
                        loadUsers();
                    } else {
                        alert(`❌ Ошибка: ${data.error}`);
                    }
                })
                .catch(error => {
                    alert(`❌ Ошибка соединения: ${error.message}`);
                })
                .finally(() => {
                    submitButton.textContent = originalText;
                    submitButton.disabled = false;
                });
            });
            
            // Handle edit form submission
            document.getElementById('edit-user-form').addEventListener('submit', function(e) {
                e.preventDefault();
                
                const formData = new FormData(this);
                const data = Object.fromEntries(formData.entries());
                const userId = data.user_id;
                
                // Show loading state
                const submitButton = this.querySelector('button[type="submit"]');
                const originalText = submitButton.textContent;
                submitButton.textContent = 'Сохранение...';
                submitButton.disabled = true;
                
                fetch(`/api/reports/simple-update-user/${userId}/`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify(data)
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Show success message
                        alert(`✅ ${data.message}`);
                        
                        // Close modal
                        closeEditUserModal();
                        
                        // Reload users list
                        loadUsers();
                    } else {
                        alert(`❌ Ошибка: ${data.error}`);
                    }
                })
                .catch(error => {
                    alert(`❌ Ошибка соединения: ${error.message}`);
                })
                .finally(() => {
                    submitButton.textContent = originalText;
                    submitButton.disabled = false;
                });
            });
            
            function editUser(userId) {
                // Находим пользователя в списке
                const userRow = document.querySelector(`tr[data-user-id="${userId}"]`);
                if (!userRow) {
                    alert('Пользователь не найден');
                    return;
                }
                
                // Получаем данные пользователя из таблицы
                const username = userRow.querySelector('td:nth-child(2) .text-sm.font-medium').textContent;
                const fullName = userRow.querySelector('td:nth-child(2) .text-sm.text-gray-500').textContent;
                const [firstName, lastName] = fullName.split(' ');
                const role = userRow.querySelector('td:nth-child(3) span').textContent.toLowerCase();
                const email = userRow.querySelector('td:nth-child(4)').textContent;
                const department = userRow.querySelector('td:nth-child(5)').textContent;
                
                // Заполняем форму редактирования
                document.getElementById('edit-user-form').style.display = 'block';
                document.getElementById('edit-user-id').value = userId;
                document.getElementById('edit-username').value = username;
                document.getElementById('edit-first-name').value = firstName || '';
                document.getElementById('edit-last-name').value = lastName || '';
                document.getElementById('edit-role').value = role;
                document.getElementById('edit-email').value = email;
                document.getElementById('edit-department').value = department;
                
                // Показываем модальное окно редактирования
                document.getElementById('edit-user-modal').classList.remove('hidden');
            }
            
            function deleteUser(userId) {
                if (confirm(`Вы уверены, что хотите удалить пользователя с ID ${userId}?`)) {
                    // Показываем индикатор загрузки
                    const deleteButton = event.target;
                    const originalText = deleteButton.textContent;
                    deleteButton.textContent = 'Удаление...';
                    deleteButton.disabled = true;
                    
                    fetch(`/api/reports/simple-delete-user/${userId}/`, {
                        method: 'DELETE',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': getCookie('csrftoken')
                        }
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            alert(`✅ ${data.message}`);
                            // Обновляем список пользователей
                            loadUsers();
                        } else {
                            alert(`❌ Ошибка: ${data.error}`);
                        }
                    })
                    .catch(error => {
                        alert(`❌ Ошибка соединения: ${error.message}`);
                    })
                    .finally(() => {
                        deleteButton.textContent = originalText;
                        deleteButton.disabled = false;
                    });
                }
            }
            
            function getCookie(name) {
                let cookieValue = null;
                if (document.cookie && document.cookie !== '') {
                    const cookies = document.cookie.split(';');
                    for (let i = 0; i < cookies.length; i++) {
                        const cookie = cookies[i].trim();
                        if (cookie.substring(0, name.length + 1) === (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }
            
            console.log('Improved user management page loaded');
        </script>
    </body>
    </html>
    """
