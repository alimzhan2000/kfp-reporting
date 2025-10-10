"""
Django settings for kfp_reporting project.
"""

from pathlib import Path
from decouple import config
import dj_database_url
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-railway-production-key-2024')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

# ALLOWED_HOSTS для Railway - максимально открытая конфигурация
ALLOWED_HOSTS = ['*']  # Разрешаем все хосты для Railway

# Дополнительно добавляем Railway домены
if 'RAILWAY_PUBLIC_DOMAIN' in os.environ:
    ALLOWED_HOSTS.append(os.environ['RAILWAY_PUBLIC_DOMAIN'])

# Принудительно добавляем все возможные Railway домены
ALLOWED_HOSTS.extend([
    '*.up.railway.app',
    '*.railway.app',
    'web-production-ed541.up.railway.app'
])

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'corsheaders',
    'django_filters',  # Восстановлено
]

LOCAL_APPS = [
    'accounts',
    'reports',
    'data_upload',  # Восстановлено
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# ПОЛНЫЙ MIDDLEWARE ДЛЯ DJANGO ADMIN И API
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'kfp_reporting.middleware.DisableCSRFForAPI',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# CSRF settings - Railway domains
CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', default='http://localhost:3000').split(',')
CSRF_TRUSTED_ORIGINS.extend([
    'https://*.up.railway.app',
    'https://*.railway.app',
    'https://web-production-ed541.up.railway.app'
])

ROOT_URLCONF = 'kfp_reporting.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'kfp_reporting.wsgi.application'

# Database - УПРОЩЕННАЯ КОНФИГУРАЦИЯ ДЛЯ RAILWAY
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL', default='sqlite:///db.sqlite3'),
        conn_max_age=600,
    )
}

# Минимальные настройки для PostgreSQL на Railway
if 'postgresql' in DATABASES['default']['ENGINE']:
    DATABASES['default']['OPTIONS'] = {
        'connect_timeout': 10,
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Asia/Almaty'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Frontend build directory
FRONTEND_BUILD_DIR = BASE_DIR / 'frontend' / 'build'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
    FRONTEND_BUILD_DIR / 'static',  # React build static files
]

# WhiteNoise configuration for serving static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# CORS settings
CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', default='http://localhost:3000').split(',')
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = config('CORS_ALLOW_ALL_ORIGINS', default=False, cast=bool)

# Для Railway health check
CORS_ALLOW_ALL_ORIGINS = True  # Временно для health check

# Session settings
SESSION_COOKIE_SAMESITE = config('SESSION_COOKIE_SAMESITE', default='Lax')
SESSION_COOKIE_HTTPONLY = config('SESSION_COOKIE_HTTPONLY', default=True, cast=bool)
SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=False, cast=bool)
CSRF_COOKIE_SAMESITE = config('CSRF_COOKIE_SAMESITE', default='Lax')
CSRF_COOKIE_HTTPONLY = config('CSRF_COOKIE_HTTPONLY', default=True, cast=bool)
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=False, cast=bool)

# Custom user model
AUTH_USER_MODEL = 'accounts.User'

# File upload settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB

# Railway specific settings
if 'RAILWAY_STATIC_URL' in os.environ:
    railway_static_url = os.environ['RAILWAY_STATIC_URL']
    # Убеждаемся, что STATIC_URL заканчивается на слэш
    if not railway_static_url.endswith('/'):
        railway_static_url += '/'
    STATIC_URL = railway_static_url

# Security settings for production
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# ПРИНУДИТЕЛЬНО УСТАНАВЛИВАЕМ ПРАВИЛЬНЫЙ STATIC_URL
# Это гарантирует, что STATIC_URL всегда заканчивается на слэш
if not STATIC_URL.endswith('/'):
    STATIC_URL = STATIC_URL + '/'

