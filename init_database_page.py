def get_init_database_page():
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
                        Перед созданием пользователей необходимо инициализировать базу данных.
                        Это применит миграции Django и создаст необходимые таблицы.
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
                statusDiv.innerHTML = 'Инициализация базы данных...';
                
                // Redirect to initialization API
                window.location.href = '/api/reports/simple-force-initialize/';
            }
            
            function goToUserManagement() {
                window.location.href = '/user-management/';
            }
            
            console.log('Init database page loaded');
        </script>
    </body>
    </html>
    """
