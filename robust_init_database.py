def get_robust_init_database_page():
    return """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Инициализация базы данных</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-50">
        <div class="min-h-screen flex items-center justify-center">
            <div class="max-w-md w-full bg-white rounded-lg shadow-md p-6">
                <div class="text-center">
                    <h1 class="text-2xl font-bold text-gray-900 mb-4">Инициализация базы данных</h1>
                    <p class="text-gray-600 mb-6">
                        Нажмите кнопку ниже для инициализации базы данных.
                        Это создаст необходимые таблицы и демо-пользователей.
                    </p>
                    
                    <div class="space-y-4">
                        <button onclick="initializeDatabase()" 
                                class="w-full bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors">
                            🔧 Инициализировать базу данных
                        </button>
                        
                        <button onclick="goToUserManagement()" 
                                class="w-full bg-gray-600 text-white px-4 py-2 rounded-md hover:bg-gray-700 transition-colors">
                            👤 Перейти к управлению пользователями
                        </button>
                    </div>
                    
                    <div id="status" class="mt-4 text-sm"></div>
                </div>
            </div>
        </div>

        <script>
            function initializeDatabase() {
                const statusDiv = document.getElementById('status');
                statusDiv.innerHTML = '<div class="text-blue-600">Инициализация базы данных...</div>';
                
                // Выполняем инициализацию через простой POST запрос
                fetch('/robust-init-database-action/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify({})
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        statusDiv.innerHTML = '<div class="text-green-600">✅ База данных успешно инициализирована!</div>';
                        setTimeout(() => {
                            window.location.href = '/user-management/';
                        }, 2000);
                    } else {
                        statusDiv.innerHTML = '<div class="text-red-600">❌ Ошибка: ' + data.error + '</div>';
                    }
                })
                .catch(error => {
                    statusDiv.innerHTML = '<div class="text-red-600">❌ Ошибка соединения: ' + error.message + '</div>';
                });
            }
            
            function goToUserManagement() {
                window.location.href = '/user-management/';
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
            
            console.log('Robust init database page loaded');
        </script>
    </body>
    </html>
    """
