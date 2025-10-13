"""
Страница авторизации для KFP Reporting
"""
from django.http import HttpResponse

def get_login_page():
    """Возвращает страницу авторизации"""
    return """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>KFP Reporting - Вход в систему</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gradient-to-br from-green-50 to-blue-50 min-h-screen flex items-center justify-center">
        <div class="max-w-md w-full space-y-8 p-8">
            <!-- Header -->
            <div class="text-center">
                <div class="mx-auto h-16 w-16 bg-green-600 rounded-full flex items-center justify-center">
                    <span class="text-white text-2xl">🌾</span>
                </div>
                <h2 class="mt-6 text-3xl font-bold text-gray-900">KFP Reporting</h2>
                <p class="mt-2 text-sm text-gray-600">Система отчетности по сельскохозяйственным данным</p>
            </div>

            <!-- Login Form -->
            <form class="mt-8 space-y-6" id="loginForm">
                <div class="space-y-4">
                    <div>
                        <label for="username" class="block text-sm font-medium text-gray-700">Имя пользователя</label>
                        <input id="username" name="username" type="text" required 
                               class="mt-1 appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-green-500 focus:border-green-500 focus:z-10 sm:text-sm" 
                               placeholder="Введите имя пользователя">
                    </div>
                    <div>
                        <label for="password" class="block text-sm font-medium text-gray-700">Пароль</label>
                        <input id="password" name="password" type="password" required 
                               class="mt-1 appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-green-500 focus:border-green-500 focus:z-10 sm:text-sm" 
                               placeholder="Введите пароль">
                    </div>
                </div>

                <div class="flex items-center justify-between">
                    <div class="flex items-center">
                        <input id="remember-me" name="remember-me" type="checkbox" 
                               class="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded">
                        <label for="remember-me" class="ml-2 block text-sm text-gray-900">Запомнить меня</label>
                    </div>
                    <div class="text-sm">
                        <a href="#" class="font-medium text-green-600 hover:text-green-500">Забыли пароль?</a>
                    </div>
                </div>

                <div>
                    <button type="submit" 
                            class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 transition-colors">
                        <span class="absolute left-0 inset-y-0 flex items-center pl-3">
                            <svg class="h-5 w-5 text-green-500 group-hover:text-green-400" fill="currentColor" viewBox="0 0 20 20">
                                <path fill-rule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clip-rule="evenodd"></path>
                            </svg>
                        </span>
                        Войти в систему
                    </button>
                </div>

            </form>

            <!-- Error message -->
            <div id="error-message" class="hidden bg-red-50 border border-red-200 rounded-md p-4">
                <div class="flex">
                    <div class="flex-shrink-0">
                        <svg class="h-5 w-5 text-red-400" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
                        </svg>
                    </div>
                    <div class="ml-3">
                        <p class="text-sm text-red-800" id="error-text"></p>
                    </div>
                </div>
            </div>
        </div>

        <script>
            document.getElementById('loginForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                
                const username = document.getElementById('username').value;
                const password = document.getElementById('password').value;
                const errorDiv = document.getElementById('error-message');
                const errorText = document.getElementById('error-text');
                
                // Hide error message
                errorDiv.classList.add('hidden');
                
                try {
                    // Real authentication with API
                    const response = await fetch('/api/auth/login/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            username: username,
                            password: password
                        })
                    });
                    
                    const data = await response.json();
                    
                    if (data.success) {
                        // Store user info in localStorage
                        localStorage.setItem('kfp_user', JSON.stringify({
                            username: data.user.username,
                            role: data.user.role,
                            id: data.user.id,
                            first_name: data.user.first_name,
                            last_name: data.user.last_name,
                            email: data.user.email,
                            is_staff: data.user.is_staff,
                            is_superuser: data.user.is_superuser,
                            loginTime: new Date().toISOString()
                        }));
                        
                        // Redirect to dashboard
                        window.location.href = '/dashboard/';
                    } else {
                        errorText.textContent = data.error || 'Ошибка аутентификации';
                        errorDiv.classList.remove('hidden');
                    }
                } catch (error) {
                    console.error('Login error:', error);
                    errorText.textContent = 'Ошибка подключения к серверу';
                    errorDiv.classList.remove('hidden');
                }
            });

            // Check if user is already logged in via server session
            async function checkAuthStatus() {
                try {
                    const response = await fetch('/api/auth/status/', {
                        method: 'GET',
                        credentials: 'include'  // Include cookies for session
                    });
                    
                    const data = await response.json();
                    
                    if (data.success && data.authenticated) {
                        // Store user info in localStorage for client-side use
                        localStorage.setItem('kfp_user', JSON.stringify(data.user));
                        window.location.href = '/dashboard/';
                    }
                } catch (error) {
                    console.log('Auth check failed:', error);
                    // Clear any stale localStorage data
                    localStorage.removeItem('kfp_user');
                }
            }
            
            // Check authentication status on page load
            checkAuthStatus();
        </script>
    </body>
    </html>
    """
