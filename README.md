# Reporting KFP

Веб-портал для анализа сельскохозяйственных данных с возможностью загрузки CSV/XLSX файлов и генерации интерактивных отчетов.

## Технологический стек

- **Backend**: Django 4.2, Django REST Framework
- **Frontend**: React 18, Tailwind CSS, Recharts
- **База данных**: PostgreSQL
- **Контейнеризация**: Docker, Docker Compose

## Функциональность

### Модуль загрузки данных
- Загрузка файлов CSV и XLSX
- Автоматический парсинг и валидация данных
- Извлечение данных по обязательным колонкам:
  - Поле
  - Год
  - Площадь посева
  - Урожайность (ц/га)
  - Культура
  - Сорт
  - Конечный продукт

### Система отчетов
1. **Сравнительный отчет по урожайности**
   - Сравнение по полям, годам, культурам, сортам
   - Гистограммы и линейные графики
   - Интерактивные фильтры

2. **Отчет по эффективности полей**
   - Тепловая карта с цветовым кодированием
   - Рейтинг полей по урожайности
   - Статистика производительности

3. **Отчет по производительности сортов**
   - Сравнение сортов в рамках культур
   - Столбчатые диаграммы
   - Детальная статистика

### Система аутентификации
- **Администратор**: создание учетных записей, полный функционал
- **Руководство**: загрузка файлов, просмотр отчетов

## Быстрый старт

### Предварительные требования
- Docker и Docker Compose
- Git

### Установка и запуск

1. **Клонирование репозитория**
```bash
git clone <repository-url>
cd kfp-reporting
```

2. **Запуск с Docker Compose**
```bash
docker-compose up --build
```

3. **Создание суперпользователя**
```bash
docker-compose exec backend python manage.py createsuperuser
```

4. **Доступ к приложению**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/api/
- Django Admin: http://localhost:8000/admin/

### Локальная разработка

#### Backend (Django)

1. **Установка зависимостей**
```bash
pip install -r requirements.txt
```

2. **Настройка базы данных**
```bash
# Создайте базу данных PostgreSQL
# Скопируйте env.example в .env и настройте DATABASE_URL
cp env.example .env
```

3. **Применение миграций**
```bash
python manage.py migrate
```

4. **Создание суперпользователя**
```bash
python manage.py createsuperuser
```

5. **Запуск сервера**
```bash
python manage.py runserver
```

#### Frontend (React)

1. **Переход в директорию frontend**
```bash
cd frontend
```

2. **Установка зависимостей**
```bash
npm install
```

3. **Запуск приложения**
```bash
npm start
```

## Структура проекта

```
kfp-reporting/
├── accounts/                 # Модуль аутентификации
├── data_upload/             # Модуль загрузки файлов
├── reports/                 # Модуль отчетов
├── frontend/                # React приложение
│   ├── src/
│   │   ├── components/      # React компоненты
│   │   ├── pages/          # Страницы приложения
│   │   ├── contexts/       # React контексты
│   │   └── services/       # API сервисы
│   └── public/
├── kfp_reporting/          # Основные настройки Django
├── media/                  # Загруженные файлы
├── static/                 # Статические файлы
├── docker-compose.yml      # Docker Compose конфигурация
├── Dockerfile             # Docker образ для backend
└── requirements.txt       # Python зависимости
```

## API Endpoints

### Аутентификация
- `POST /api/auth/login/` - Вход в систему
- `POST /api/auth/logout/` - Выход из системы
- `GET /api/auth/profile/` - Профиль пользователя
- `POST /api/auth/create/` - Создание пользователя (только админ)
- `GET /api/auth/list/` - Список пользователей (только админ)

### Загрузка данных
- `POST /api/upload/file/` - Загрузка файла
- `GET /api/upload/history/` - История загрузок
- `GET /api/upload/status/{id}/` - Статус загрузки

### Отчеты
- `GET /api/reports/data/` - Список данных с фильтрацией
- `GET /api/reports/yield-comparison/` - Сравнительный отчет
- `GET /api/reports/field-efficiency/` - Отчет по эффективности полей
- `GET /api/reports/variety-performance/` - Отчет по сортам
- `GET /api/reports/dashboard-stats/` - Статистика для дашборда

## Переменные окружения

Создайте файл `.env` на основе `env.example`:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=postgresql://username:password@localhost:5432/kfp_reporting
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

## Разработка

### Создание миграций
```bash
python manage.py makemigrations
python manage.py migrate
```

### Создание тестовых данных
```bash
python manage.py shell
# Используйте Django shell для создания тестовых данных
```

### Сборка для продакшена
```bash
# Backend
docker build -t kfp-reporting-backend .

# Frontend
cd frontend
npm run build
```

## Лицензия

MIT License

## Поддержка

Для получения поддержки обращайтесь к команде разработки.

