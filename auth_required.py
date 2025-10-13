"""
Декоратор для проверки авторизации пользователей
"""
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
import functools

def auth_required(view_func):
    """
    Декоратор для проверки авторизации пользователя.
    Если пользователь не авторизован, показывает страницу с ошибкой авторизации.
    """
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            # Возвращаем страницу с ошибкой авторизации
            return HttpResponse(get_auth_error_page(), content_type="text/html")
    
    return wrapper

def get_auth_error_page():
    """Страница с ошибкой авторизации"""
    return """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Требуется авторизация - KFP Reporting</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            body {
                font-family: 'Inter', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .container {
                max-width: 500px;
                margin: 0 auto;
                padding: 2rem;
            }
            .card {
                background-color: #ffffff;
                border-radius: 1rem;
                box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
                padding: 3rem;
                text-align: center;
            }
            .icon {
                width: 80px;
                height: 80px;
                margin: 0 auto 2rem;
                background-color: #fee2e2;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .icon svg {
                width: 40px;
                height: 40px;
                color: #dc2626;
            }
            .btn {
                background-color: #059669;
                color: white;
                padding: 0.75rem 2rem;
                border-radius: 0.5rem;
                text-decoration: none;
                display: inline-block;
                font-weight: 600;
                transition: background-color 0.2s;
                margin-top: 1.5rem;
            }
            .btn:hover {
                background-color: #047857;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="card">
                <div class="icon">
                    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
                    </svg>
                </div>
                
                <h1 class="text-2xl font-bold text-gray-900 mb-4">
                    Требуется авторизация
                </h1>
                
                <p class="text-gray-600 mb-6">
                    Для доступа к этой странице необходимо войти в систему.
                </p>
                
                <p class="text-gray-500 text-sm mb-8">
                    Пожалуйста, авторизуйтесь, чтобы продолжить работу с системой KFP Reporting.
                </p>
                
                <a href="/login/" class="btn">
                    Войти в систему
                </a>
            </div>
        </div>
        
        <script>
            // Автоматическое перенаправление через 5 секунд
            setTimeout(function() {
                window.location.href = '/login/';
            }, 5000);
        </script>
    </body>
    </html>
    """
