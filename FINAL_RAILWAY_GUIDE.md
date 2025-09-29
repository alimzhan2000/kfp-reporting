# 🎯 Финальная инструкция для нового проекта Railway

## 🚀 **Два способа создания нового проекта**

### **Способ 1: Автоматический (рекомендуется)**

```bash
# Установите токен Railway
export RAILWAY_TOKEN=ваш-новый-токен

# Запустите автоматический скрипт
./setup-new-railway.sh
```

**Скрипт автоматически:**
- ✅ Создаст новый проект из GitHub
- ✅ Добавит PostgreSQL базу данных
- ✅ Настроит все переменные окружения
- ✅ Задеплоит приложение
- ✅ Получит публичный URL
- ✅ Обновит CORS настройки

### **Способ 2: Ручной (через Dashboard)**

1. **Откройте Railway Dashboard:**
   - https://railway.app/dashboard
   - Нажмите **"+ New Project"**

2. **Выберите источник:**
   - **"Deploy from GitHub repo"**
   - Выберите: `alimzhan2000/kfp-reporting`
   - Нажмите **"Deploy Now"**

3. **Добавьте PostgreSQL:**
   - Нажмите **"+ New"** → **"Database"** → **"PostgreSQL"**

4. **Настройте переменные окружения:**
   - Перейдите в **"Variables"**
   - Добавьте переменные из `NEW_RAILWAY_SETUP.md`

5. **Включите публичный доступ:**
   - **Settings** → **Networking** → **"Public Networking"**

## 📋 **Переменные окружения для нового проекта**

### **Основные настройки:**
```
SECRET_KEY = django-insecure-ваш-секретный-ключ
DEBUG = False
ALLOWED_HOSTS = *
DJANGO_SETTINGS_MODULE = kfp_reporting.settings
```

### **CORS настройки (обновите после получения домена):**
```
CORS_ALLOWED_ORIGINS = https://ваш-новый-домен.up.railway.app
CORS_TRUSTED_ORIGINS = https://ваш-новый-домен.up.railway.app
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = False
```

### **Cookie настройки:**
```
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = None
CSRF_COOKIE_SAMESITE = None
SESSION_COOKIE_HTTPONLY = False
CSRF_COOKIE_HTTPONLY = False
```

## 🔧 **После создания проекта**

### **1. Выполните миграции:**
```bash
# В Railway Dashboard → Deployments → Terminal
python manage.py migrate
python manage.py createsuperuser
python init_db.py
```

### **2. Проверьте результат:**
- **Главная**: `https://ваш-домен.up.railway.app/`
- **Health Check**: `https://ваш-домен.up.railway.app/api/health/`
- **API**: `https://ваш-домен.up.railway.app/api/reports/dashboard-stats/`
- **Админка**: `https://ваш-домен.up.railway.app/admin/`

## 🎯 **Преимущества нового проекта**

- ✅ **Чистая конфигурация** - без старых ошибок
- ✅ **Правильные настройки** - все с нуля
- ✅ **Автоматические миграции** - встроены в startCommand
- ✅ **Улучшенная стабильность** - больше workers и timeout
- ✅ **Простота настройки** - пошаговая инструкция

## 🆘 **Если что-то не работает**

1. **Проверьте логи**: Railway Dashboard → Deployments → Logs
2. **Проверьте переменные**: Railway Dashboard → Variables
3. **Проверьте базу данных**: Railway Dashboard → Database
4. **Перезапустите сервис**: Railway Dashboard → Deployments → Redeploy

## 📞 **Поддержка**

- **Подробная инструкция**: `NEW_RAILWAY_SETUP.md`
- **Автоматический скрипт**: `setup-new-railway.sh`
- **Старая инструкция**: `RAILWAY_SETUP_GUIDE.md`

**Рекомендуется использовать автоматический способ для быстрой настройки!** 🚀
