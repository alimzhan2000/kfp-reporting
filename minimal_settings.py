# Минимальные настройки Django для Railway
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Базовые настройки
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-railway-minimal-2024')
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

# Разрешаем все хосты
ALLOWED_HOSTS = ['*']

# Минимальные приложения
INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# Минимальный middleware
MIDDLEWARE = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

# База данных
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Статические файлы
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# URL конфигурация
ROOT_URLCONF = 'kfp_reporting.minimal_urls'

# Интернационализация
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Asia/Almaty'
USE_I18N = True
USE_TZ = True

# Безопасность
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
