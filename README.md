![image](https://github.com/user-attachments/assets/5bc9d0d1-161d-41b2-a32b-d726af762869)# ClinicAPI

## Описание проекта

**ClinicAPI** — серверная часть информационной системы косметологической клиники, разработанная на FastAPI с использованием SQLAlchemy в рамках дисциплины "Базы данных". Проект предоставляет REST API, возвращающий результаты определенных SQL запросов, производимыми над базой данных клинику.

## Требования

- Python 3.10+
- PostgreSQL 12+ (или другая поддерживаемая СУБД)
- Установленный `pip`

## Установка и настройка

### 1. Клонирование репозитория

```bash
git clone (https://github.com/purpurrya/ClinicAPI).git
cd ClinicAPI
```

### 2. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Применение миграций

Проект использует Alembic для управления миграциями базы данных:

1. Инициализация (если требуется):
```bash
alembic init alembic
```

2. Создание новой миграции (при изменении моделей):
```bash
alembic revision --autogenerate -m "Описание изменений"
```

3. Применение миграций:
```bash
alembic upgrade head
```

## Запуск приложения

```bash
uvicorn main:app --reload
```

Приложение будет доступно по адресу: `http://localhost:8000`

## Документация API

После запуска приложения доступны следующие интерфейсы документации:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
