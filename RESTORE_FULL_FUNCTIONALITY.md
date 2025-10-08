# 🔄 Восстановление полного функционала после успешного деплоя

## Текущее состояние (минимальная версия)
- ✅ Только базовые зависимости Django
- ✅ Отключены: django_filters, data_upload, Pillow, openpyxl, celery, redis
- ✅ Используется runserver вместо gunicorn
- ✅ Приложение должно запускаться без ошибок

## После успешного деплоя

### Шаг 1: Восстановить полный requirements.txt
Замените содержимое `requirements.txt` на:
```
Django==4.2.7
djangorestframework==3.14.0
django-cors-headers==4.3.1
psycopg2-binary==2.9.9
numpy==1.24.3
pandas==2.0.3
openpyxl==3.1.2
python-decouple==3.8
Pillow==10.1.0
django-filter==23.5
celery==5.3.4
redis==5.0.1
whitenoise==6.6.0
gunicorn==21.2.0
dj-database-url==2.1.0
setuptools>=65.0.0
wheel>=0.38.0
```

### Шаг 2: Восстановить приложения в settings.py
Раскомментируйте в `kfp_reporting/settings.py`:
```python
THIRD_PARTY_APPS = [
    'rest_framework',
    'corsheaders',
    'django_filters',  # Раскомментировать
]

LOCAL_APPS = [
    'accounts',
    'reports',
    'data_upload',  # Раскомментировать
]
```

### Шаг 3: Восстановить URLs
Раскомментируйте в `kfp_reporting/urls.py`:
```python
path('api/upload/', include('data_upload.urls')),  # Раскомментировать
```

### Шаг 4: Восстановить gunicorn
Замените в `railway.json`:
```json
"startCommand": "python manage.py migrate && gunicorn kfp_reporting.wsgi:application --bind 0.0.0.0:$PORT"
```

### Шаг 5: Восстановить REST_FRAMEWORK настройки
Добавьте в `kfp_reporting/settings.py`:
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}
```

## Проверка
После восстановления все функции должны работать:
- ✅ Загрузка файлов (CSV, Excel)
- ✅ Фильтрация и поиск
- ✅ Обработка изображений
- ✅ Фоновые задачи (celery)
- ✅ Production-ready gunicorn
