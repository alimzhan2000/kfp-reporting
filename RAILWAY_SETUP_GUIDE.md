# 🚀 Пошаговая инструкция настройки Railway

## 📋 **Что нужно сделать в Railway Dashboard**

### **Шаг 1: Откройте Railway Dashboard**
1. Перейдите на https://railway.app/dashboard
2. Войдите в ваш аккаунт
3. Найдите проект `kfp-reporting` (или создайте новый)

### **Шаг 2: Настройте PostgreSQL базу данных**
1. В вашем проекте нажмите **"+ New"**
2. Выберите **"Database"** → **"PostgreSQL"**
3. Дождитесь создания базы данных
4. Скопируйте **DATABASE_URL** (он будет автоматически добавлен)

### **Шаг 3: Настройте переменные окружения**
В разделе **"Variables"** добавьте следующие переменные:

#### **Основные настройки Django:**
```
SECRET_KEY = django-insecure-ваш-секретный-ключ-здесь
DEBUG = False
ALLOWED_HOSTS = *
DJANGO_SETTINGS_MODULE = kfp_reporting.settings
```

#### **CORS настройки:**
```
CORS_ALLOWED_ORIGINS = https://ваш-домен.up.railway.app
CORS_TRUSTED_ORIGINS = https://ваш-домен.up.railway.app
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = False
```

#### **Cookie настройки для HTTPS:**
```
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = None
CSRF_COOKIE_SAMESITE = None
SESSION_COOKIE_HTTPONLY = False
CSRF_COOKIE_HTTPONLY = False
```

### **Шаг 4: Настройте публичный доступ**
1. В разделе **"Settings"** → **"Networking"**
2. Включите **"Public Networking"**
3. Скопируйте **публичный URL** (например: `https://kfp-reporting-production.up.railway.app`)

### **Шаг 5: Обновите CORS настройки**
Замените `https://ваш-домен.up.railway.app` на ваш реальный публичный URL в переменных:
```
CORS_ALLOWED_ORIGINS = https://kfp-reporting-production.up.railway.app
CORS_TRUSTED_ORIGINS = https://kfp-reporting-production.up.railway.app
```

### **Шаг 6: Выполните миграции базы данных**
1. В разделе **"Deployments"** нажмите на последний деплой
2. Откройте **"Terminal"** (консоль)
3. Выполните команды по порядку:

```bash
# Выполните миграции
python manage.py migrate

# Создайте суперпользователя
python manage.py createsuperuser
# Введите username, email, password

# Загрузите тестовые данные (опционально)
python init_db.py
```

### **Шаг 7: Проверьте работоспособность**
Откройте в браузере:
- **Главная страница**: `https://ваш-домен.up.railway.app/`
- **Health Check**: `https://ваш-домен.up.railway.app/api/health/`
- **API**: `https://ваш-домен.up.railway.app/api/reports/dashboard-stats/`
- **Админка**: `https://ваш-домен.up.railway.app/admin/`

## 🔧 **Возможные проблемы и решения**

### **Проблема 1: API возвращает 404**
**Решение**: Выполните миграции базы данных (Шаг 6)

### **Проблема 2: CORS ошибки**
**Решение**: Проверьте правильность URL в CORS настройках

### **Проблема 3: Приложение не запускается**
**Решение**: Проверьте логи в разделе "Deployments" → "Logs"

### **Проблема 4: База данных недоступна**
**Решение**: Убедитесь, что PostgreSQL сервис запущен и DATABASE_URL настроен

## 📊 **Доступные endpoints после настройки**

- **Главная**: `https://ваш-домен.up.railway.app/`
- **Health Check**: `https://ваш-домен.up.railway.app/api/health/`
- **API**: `https://ваш-домен.up.railway.app/api/`
- **Админка**: `https://ваш-домен.up.railway.app/admin/`
- **Загрузка файлов**: `https://ваш-домен.up.railway.app/api/upload/file/`
- **Отчеты**: `https://ваш-домен.up.railway.app/api/reports/`

## 🎯 **Финальная проверка**

После выполнения всех шагов:
1. ✅ Приложение запускается без ошибок
2. ✅ База данных подключена и мигрирована
3. ✅ API endpoints доступны
4. ✅ Админка работает
5. ✅ Публичный доступ настроен

**Готово! Ваше приложение полностью настроено и готово к использованию!** 🎉
