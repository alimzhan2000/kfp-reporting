# 🤖 Автоматическая настройка Railway

## 🚀 **Быстрый запуск (автоматически)**

### **Шаг 1: Установите токен**
```bash
export RAILWAY_TOKEN=2d3d3307-71a4-4a0a-aa81-7c8b45ffa17f
```

### **Шаг 2: Запустите автоматический скрипт**
```bash
chmod +x auto-setup-railway.sh
./auto-setup-railway.sh
```

**Скрипт автоматически:**
- ✅ Настроит все переменные окружения
- ✅ Задеплоит приложение
- ✅ Выполнит миграции базы данных
- ✅ Создаст суперпользователя
- ✅ Загрузит тестовые данные
- ✅ Проверит работоспособность

---

## 🔧 **Ручная настройка (если автоматическая не работает)**

### **Шаг 1: Настройте переменные окружения**
```bash
# Установите токен
export RAILWAY_TOKEN=2d3d3307-71a4-4a0a-aa81-7c8b45ffa17f

# Основные настройки
npx -y @railway/cli variables --set 'SECRET_KEY=django-insecure-ваш-ключ' --service kfp-reporting
npx -y @railway/cli variables --set 'DEBUG=False' --service kfp-reporting
npx -y @railway/cli variables --set 'ALLOWED_HOSTS=*' --service kfp-reporting

# CORS настройки
npx -y @railway/cli variables --set 'CORS_ALLOWED_ORIGINS=https://kfp-reporting-production.up.railway.app' --service kfp-reporting
npx -y @railway/cli variables --set 'CORS_TRUSTED_ORIGINS=https://kfp-reporting-production.up.railway.app' --service kfp-reporting
npx -y @railway/cli variables --set 'CORS_ALLOW_CREDENTIALS=True' --service kfp-reporting
npx -y @railway/cli variables --set 'CORS_ALLOW_ALL_ORIGINS=False' --service kfp-reporting

# Cookie настройки
npx -y @railway/cli variables --set 'SESSION_COOKIE_SECURE=True' --service kfp-reporting
npx -y @railway/cli variables --set 'CSRF_COOKIE_SECURE=True' --service kfp-reporting
npx -y @railway/cli variables --set 'SESSION_COOKIE_SAMESITE=None' --service kfp-reporting
npx -y @railway/cli variables --set 'CSRF_COOKIE_SAMESITE=None' --service kfp-reporting
npx -y @railway/cli variables --set 'SESSION_COOKIE_HTTPONLY=False' --service kfp-reporting
npx -y @railway/cli variables --set 'CSRF_COOKIE_HTTPONLY=False' --service kfp-reporting
```

### **Шаг 2: Задеплойте приложение**
```bash
git add .
git commit -m "Configure Railway deployment"
git push

npx -y @railway/cli up --service kfp-reporting --ci --detach
```

### **Шаг 3: Выполните миграции**
```bash
# Дождитесь завершения деплоя (2-3 минуты)
sleep 180

# Выполните миграции
npx -y @railway/cli run --service kfp-reporting python manage.py migrate

# Создайте суперпользователя
npx -y @railway/cli run --service kfp-reporting python manage.py createsuperuser

# Загрузите тестовые данные
npx -y @railway/cli run --service kfp-reporting python init_db.py
```

### **Шаг 4: Проверьте результат**
```bash
# Проверьте доступность
curl https://kfp-reporting-production.up.railway.app/
curl https://kfp-reporting-production.up.railway.app/api/health/
curl https://kfp-reporting-production.up.railway.app/api/reports/dashboard-stats/
```

---

## 🎯 **Ожидаемый результат**

После выполнения всех шагов:
- ✅ **Главная страница**: `https://kfp-reporting-production.up.railway.app/`
- ✅ **Health Check**: `https://kfp-reporting-production.up.railway.app/api/health/`
- ✅ **API**: `https://kfp-reporting-production.up.railway.app/api/reports/dashboard-stats/`
- ✅ **Админка**: `https://kfp-reporting-production.up.railway.app/admin/`

## 🆘 **Если что-то не работает**

1. **Проверьте логи**: Railway Dashboard → Deployments → Logs
2. **Проверьте переменные**: Railway Dashboard → Variables
3. **Проверьте базу данных**: Railway Dashboard → Database
4. **Перезапустите сервис**: Railway Dashboard → Deployments → Redeploy

## 📞 **Поддержка**

Если автоматическая настройка не работает, используйте ручную настройку через Railway Dashboard согласно `RAILWAY_SETUP_GUIDE.md`.
