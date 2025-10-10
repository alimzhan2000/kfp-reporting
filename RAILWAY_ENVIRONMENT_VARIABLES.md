# 🔧 Переменные окружения для Railway

## 🚨 Проблема:
- ✅ Django запускается без ошибок
- ✅ Все middleware настроены правильно
- ❌ Приложение не отвечает на HTTP запросы
- ❌ "Application failed to respond"

## 🔍 Возможные причины:
1. Отсутствуют переменные окружения в Railway
2. Django не может найти SECRET_KEY
3. Неправильные настройки DEBUG
4. Проблемы с ALLOWED_HOSTS

## ✅ Необходимые переменные окружения в Railway:

### ОБЯЗАТЕЛЬНЫЕ:
```bash
SECRET_KEY=django-insecure-railway-production-key-2024
DEBUG=False
DATABASE_URL=postgresql://user:password@host:port/database
```

### ОПЦИОНАЛЬНЫЕ:
```bash
ALLOWED_HOSTS=*
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
CSRF_TRUSTED_ORIGINS=https://*.up.railway.app,https://*.railway.app
```

## 🛠️ Как добавить переменные в Railway:

1. **Перейдите в Railway Dashboard**
2. **Выберите ваш проект**
3. **Перейдите в Settings → Variables**
4. **Добавьте переменные:**

| Variable | Value | Required |
|----------|-------|----------|
| `SECRET_KEY` | `django-insecure-railway-production-key-2024` | ✅ Yes |
| `DEBUG` | `False` | ✅ Yes |
| `DATABASE_URL` | `postgresql://...` | ✅ Yes |
| `ALLOWED_HOSTS` | `*` | ⚠️ Optional |
| `CORS_ALLOWED_ORIGINS` | `https://your-domain.com` | ⚠️ Optional |

## 🎯 Ожидаемый результат:
- ✅ Django найдет все необходимые переменные
- ✅ SECRET_KEY будет установлен
- ✅ DEBUG будет False для production
- ✅ Приложение должно отвечать на HTTP запросы

## 📋 Проверка в Railway:
1. Перейдите в Settings → Variables
2. Убедитесь, что все переменные добавлены
3. Проверьте, что DATABASE_URL правильно настроен
4. Перезапустите деплой после добавления переменных

## 🔄 Если проблема остается:
1. Проверьте Deploy Logs на наличие ошибок
2. Убедитесь, что DATABASE_URL корректный
3. Проверьте, что PostgreSQL сервис работает
4. Посмотрите HTTP Logs для диагностики запросов
