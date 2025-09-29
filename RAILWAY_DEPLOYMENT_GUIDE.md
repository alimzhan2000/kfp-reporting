# 🚀 Пошаговая инструкция развертывания KFP Reporting на Railway

## 📋 Предварительные требования
- Аккаунт на Railway.app
- GitHub репозиторий: https://github.com/alimzhan2000/kfp-reporting.git
- Railway CLI установлен

## 🔧 Шаг 1: Создание проекта на Railway

### 1.1 Войти в Railway Dashboard
1. Откройте https://railway.app/dashboard
2. Войдите в свой аккаунт

### 1.2 Создать новый проект
1. Нажмите **"New Project"**
2. Выберите **"Deploy from GitHub repo"**
3. Найдите и выберите репозиторий `alimzhan2000/kfp-reporting`
4. Нажмите **"Deploy Now"**

## 🗄️ Шаг 2: Настройка базы данных PostgreSQL

### 2.1 Добавить PostgreSQL сервис
1. В панели проекта нажмите **"+ New"**
2. Выберите **"Database"**
3. Выберите **"PostgreSQL"**
4. Дождитесь создания базы данных

### 2.2 Получить строку подключения
1. Кликните на созданную базу данных
2. Перейдите на вкладку **"Variables"**
3. Скопируйте значение `DATABASE_URL`

## ⚙️ Шаг 3: Настройка переменных окружения

### 3.1 Основные переменные Django
В настройках сервиса `kfp-reporting` добавьте:

```bash
SECRET_KEY=django-insecure-ваш-секретный-ключ-здесь
DEBUG=False
DJANGO_SETTINGS_MODULE=kfp_reporting.settings
ALLOWED_HOSTS=*
```

### 3.2 База данных
```bash
DATABASE_URL=postgresql://postgres:пароль@хост:порт/база_данных
```

### 3.3 CORS настройки
```bash
CORS_ALLOWED_ORIGINS=https://ваш-домен.up.railway.app
CORS_ALLOW_CREDENTIALS=True
CORS_ALLOW_ALL_ORIGINS=False
CORS_ALLOWED_HEADERS=accept,accept-encoding,authorization,content-type,dnt,origin,user-agent,x-csrftoken,x-requested-with
CORS_EXPOSE_HEADERS=content-type,x-csrftoken
CORS_PREFLIGHT_MAX_AGE=86400
CORS_TRUSTED_ORIGINS=https://ваш-домен.up.railway.app
```

### 3.4 Cookie настройки для HTTPS
```bash
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SESSION_COOKIE_SAMESITE=None
CSRF_COOKIE_SAMESITE=None
SESSION_COOKIE_HTTPONLY=False
CSRF_COOKIE_HTTPONLY=False
```

## 🚀 Шаг 4: Настройка деплоя

### 4.1 Команда запуска
В настройках сервиса установите:
```bash
Start Command: gunicorn kfp_reporting.wsgi:application --bind 0.0.0.0:$PORT
```

### 4.2 Health Check
```bash
Health Check Path: /api/
Health Check Timeout: 100
```

## 🔄 Шаг 5: Миграции и инициализация

### 5.1 Выполнить миграции
После успешного деплоя выполните:

```bash
# Через Railway CLI или в настройках сервиса
railway run python manage.py migrate
```

### 5.2 Создать суперпользователя
```bash
railway run python manage.py createsuperuser
```

### 5.3 Загрузить тестовые данные (опционально)
```bash
railway run python init_db.py
```

## 🌐 Шаг 6: Настройка публичного доступа

### 6.1 Получить домен
1. В настройках сервиса найдите **"Domains"**
2. Нажмите **"Generate Domain"**
3. Скопируйте полученный URL

### 6.2 Обновить CORS настройки
Замените в переменных окружения:
```bash
CORS_ALLOWED_ORIGINS=https://ваш-реальный-домен.up.railway.app
CORS_TRUSTED_ORIGINS=https://ваш-реальный-домен.up.railway.app
```

### 6.3 Перезапустить сервис
После изменения переменных сервис автоматически перезапустится.

## ✅ Шаг 7: Проверка работоспособности

### 7.1 Тестирование API
```bash
# Проверка доступности
curl https://ваш-домен.up.railway.app/api/

# Проверка статистики
curl https://ваш-домен.up.railway.app/api/reports/dashboard-stats/
```

### 7.2 Проверка базы данных
1. Откройте Django Admin: `https://ваш-домен.up.railway.app/admin/`
2. Войдите с учетными данными суперпользователя
3. Проверьте наличие таблиц

## 🔧 Шаг 8: Дополнительные настройки

### 8.1 Настройка статических файлов
Добавьте переменную:
```bash
STATIC_URL=/static/
STATIC_ROOT=/app/staticfiles/
```

### 8.2 Настройка медиа файлов
```bash
MEDIA_URL=/media/
MEDIA_ROOT=/app/media/
```

## 🚨 Устранение неполадок

### Проблема: 500 Internal Server Error
**Решение:**
1. Проверьте логи в Railway Dashboard
2. Убедитесь, что все переменные окружения установлены
3. Проверьте подключение к базе данных

### Проблема: CORS ошибки
**Решение:**
1. Обновите `CORS_ALLOWED_ORIGINS` с правильным доменом
2. Убедитесь, что `CORS_ALLOW_CREDENTIALS=True`

### Проблема: База данных не подключена
**Решение:**
1. Проверьте `DATABASE_URL` в переменных окружения
2. Убедитесь, что PostgreSQL сервис запущен
3. Выполните миграции: `railway run python manage.py migrate`

## 📊 Мониторинг

### Логи приложения
1. В Railway Dashboard → ваш сервис → **"Deployments"**
2. Кликните на последний деплой
3. Просмотрите логи в реальном времени

### Метрики
1. Перейдите на вкладку **"Metrics"**
2. Мониторьте использование CPU, памяти, сети

## 🎯 Финальная проверка

После выполнения всех шагов ваше приложение должно быть доступно по адресу:
```
https://ваш-домен.up.railway.app
```

**API Endpoints:**
- Главная: `https://ваш-домен.up.railway.app/api/`
- Админка: `https://ваш-домен.up.railway.app/admin/`
- Загрузка файлов: `https://ваш-домен.up.railway.app/api/upload/file/`
- Отчеты: `https://ваш-домен.up.railway.app/api/reports/`

## 📞 Поддержка

При возникновении проблем:
1. Проверьте логи в Railway Dashboard
2. Убедитесь, что все переменные окружения установлены правильно
3. Проверьте подключение к базе данных
4. Убедитесь, что миграции выполнены успешно
