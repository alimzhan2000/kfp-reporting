# 🔧 Решения проблемы с переменной PORT в Railway

## 🚨 Проблема:
```
CommandError: "0.0.0.0:${PORT}" is not a valid port number or address:port pair.
```

Railway не может правильно разрешить переменную `${PORT}` в команде запуска.

## ✅ Решения:

### Решение 1: Python скрипт (ТЕКУЩЕЕ)
Создан скрипт `start_railway.py`, который читает переменную PORT из окружения:

```python
import os
import sys
import subprocess

def main():
    port = os.environ.get('PORT', '8000')
    cmd = [sys.executable, 'manage.py', 'runserver', f'0.0.0.0:{port}', '--noreload']
    subprocess.run(cmd, check=True)

if __name__ == '__main__':
    main()
```

**Конфигурация:**
```json
{
  "startCommand": "python start_railway.py"
}
```

### Решение 2: Без переменной PORT
Railway автоматически перенаправляет трафик на порт по умолчанию:

```json
{
  "startCommand": "python manage.py runserver --noreload"
}
```

### Решение 3: Фиксированный порт
Использовать стандартный порт Django:

```json
{
  "startCommand": "python manage.py runserver 0.0.0.0:8000 --noreload"
}
```

### Решение 4: Переменная окружения в Railway
Добавить в Railway переменные:
```
PORT=8000
```

## 🎯 Рекомендуемый порядок тестирования:

1. **Попробуйте текущее решение** (Python скрипт)
2. **Если не работает** - используйте `railway_simple.json`
3. **Если не работает** - используйте фиксированный порт
4. **Если не работает** - добавьте переменную PORT в Railway

## 📋 Файлы конфигурации:

- `railway.json` - текущая конфигурация с Python скриптом
- `railway_simple.json` - без переменной PORT
- `railway_alternative.json` - альтернативная конфигурация
- `start_railway.py` - Python скрипт для запуска

## 🔄 Как переключиться:

1. **Переименуйте файлы:**
   ```bash
   mv railway.json railway_python.json
   mv railway_simple.json railway.json
   ```

2. **Или измените конфигурацию в Railway Dashboard**

## 🚨 Важно:
- Railway автоматически управляет портами
- Django runserver подходит для тестирования
- Флаг `--noreload` обязателен для production
