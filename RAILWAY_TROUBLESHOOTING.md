# 🚨 Railway Troubleshooting Guide

## Проблема: Health Check Failure

Если Railway не проходит health check, попробуйте следующие варианты:

### Вариант 1: Отключить Health Check
1. Скопируйте содержимое `railway-no-healthcheck.json` в `railway.json`
2. Запустите новый деплой

### Вариант 2: Использовать runserver
1. Скопируйте содержимое `railway-runserver.json` в `railway.json`
2. Запустите новый деплой

### Вариант 3: Упрощенная конфигурация
1. Скопируйте содержимое `nixpacks-simple.toml` в `nixpacks.toml`
2. Запустите новый деплой

### Вариант 4: Ручная настройка в Railway Dashboard
1. Откройте Railway Dashboard → ваш проект → Settings
2. В разделе "Deploy" отключите "Health Check"
3. Или измените "Health Check Path" на `/minimal/`

## Доступные Health Check Endpoints

- `/` - главная страница (возвращает "OK")
- `/health/` - простой health check
- `/minimal/` - минимальный health check

## Проверка локально

```bash
# Запустите локально
python manage.py runserver 0.0.0.0:8000

# Проверьте endpoints
curl http://localhost:8000/
curl http://localhost:8000/health/
curl http://localhost:8000/minimal/
```

Все должны возвращать "OK".
