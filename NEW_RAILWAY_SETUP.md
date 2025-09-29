# 🆕 Создание нового проекта Railway с нуля

## 📋 **Пошаговая инструкция**

### **Шаг 1: Создание нового проекта в Railway**

1. **Откройте Railway Dashboard:**
   - Перейдите на https://railway.app/dashboard
   - Нажмите **"+ New Project"**

2. **Выберите источник:**
   - Выберите **"Deploy from GitHub repo"**
   - Выберите репозиторий: `alimzhan2000/kfp-reporting`
   - Нажмите **"Deploy Now"**

3. **Дождитесь создания проекта:**
   - Railway автоматически создаст новый проект
   - Скопируйте **Project ID** (он понадобится для CLI)

### **Шаг 2: Настройка PostgreSQL базы данных**

1. **Добавьте PostgreSQL:**
   - В новом проекте нажмите **"+ New"**
   - Выберите **"Database"** → **"PostgreSQL"**
   - Дождитесь создания базы данных

2. **Скопируйте DATABASE_URL:**
   - Railway автоматически добавит переменную `DATABASE_URL`
   - Она будет выглядеть примерно так: `postgresql://postgres:password@host:port/railway`

### **Шаг 3: Настройка переменных окружения**

В разделе **"Variables"** добавьте следующие переменные:

#### **Основные настройки Django:**
```
SECRET_KEY = django-insecure-ваш-секретный-ключ-здесь
DEBUG = False
ALLOWED_HOSTS = *
DJANGO_SETTINGS_MODULE = kfp_reporting.settings
```

#### **CORS настройки (обновите после получения домена):**
```
CORS_ALLOWED_ORIGINS = https://ваш-новый-домен.up.railway.app
CORS_TRUSTED_ORIGINS = https://ваш-новый-домен.up.railway.app
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

### **Шаг 4: Настройка публичного доступа**

1. **Включите публичный доступ:**
   - Перейдите в **"Settings"** → **"Networking"**
   - Включите **"Public Networking"**
   - Скопируйте **публичный URL** (например: `https://kfp-reporting-new.up.railway.app`)

2. **Обновите CORS настройки:**
   - Замените `https://ваш-новый-домен.up.railway.app` на ваш реальный публичный URL
   - Обновите переменные `CORS_ALLOWED_ORIGINS` и `CORS_TRUSTED_ORIGINS`

### **Шаг 5: Проверка деплоя**

1. **Проверьте статус деплоя:**
   - Перейдите в **"Deployments"**
   - Убедитесь, что деплой завершился успешно
   - Если есть ошибки, проверьте логи

2. **Проверьте доступность:**
   - Откройте ваш публичный URL
   - Должна отобразиться главная страница

### **Шаг 6: Выполнение миграций**

1. **Откройте консоль:**
   - В разделе **"Deployments"** нажмите на последний деплой
   - Откройте **"Terminal"**

2. **Выполните команды по порядку:**
   ```bash
   # Выполните миграции
   python manage.py migrate
   
   # Создайте суперпользователя
   python manage.py createsuperuser
   # Введите username, email, password
   
   # Загрузите тестовые данные (опционально)
   python init_db.py
   ```

### **Шаг 7: Финальная проверка**

Проверьте все endpoints:
- **Главная**: `https://ваш-домен.up.railway.app/`
- **Health Check**: `https://ваш-домен.up.railway.app/api/health/`
- **API**: `https://ваш-домен.up.railway.app/api/reports/dashboard-stats/`
- **Админка**: `https://ваш-домен.up.railway.app/admin/`

## 🎯 **Ожидаемый результат**

После выполнения всех шагов:
- ✅ Приложение запускается без ошибок
- ✅ База данных подключена и мигрирована
- ✅ API endpoints доступны
- ✅ Админка работает
- ✅ Публичный доступ настроен

## 🆘 **Если что-то не работает**

1. **Проверьте логи**: Railway Dashboard → Deployments → Logs
2. **Проверьте переменные**: Railway Dashboard → Variables
3. **Проверьте базу данных**: Railway Dashboard → Database
4. **Перезапустите сервис**: Railway Dashboard → Deployments → Redeploy

## 📞 **Поддержка**

Если возникнут проблемы, проверьте:
- Правильность всех переменных окружения
- Статус PostgreSQL базы данных
- Логи деплоя на наличие ошибок
- Публичный доступ в настройках Networking
