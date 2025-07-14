# ImagiQueue

[![CI](https://github.com/Maxim-Proskurin/ImagiQueue/actions/workflows/ci.yml/badge.svg)](https://github.com/Maxim-Proskurin/ImagiQueue/actions)
[![codecov](https://codecov.io/gh/Maxim-Proskurin/ImagiQueue/branch/main/graph/badge.svg)](https://codecov.io/gh/Maxim-Proskurin/ImagiQueue)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Описание

**ImagiQueue** — асинхронный REST API сервис для загрузки и обработки изображений. Поддерживает очереди задач через Celery и Redis, хранение данных в PostgreSQL, JWT-авторизацию, покрытие тестами и CI/CD.

## Функционал

- Регистрация и логин пользователя (JWT)
- Загрузка изображений (`multipart/form-data`)
- Получение статуса задачи (в очереди, в обработке, готово)
- Скачивание обработанных файлов
- История задач пользователя
- Swagger UI для тестирования API (`/docs`)
- Асинхронные эндпоинты (FastAPI)
- Фоновые задачи (Celery)
- Тесты на основные сценарии
- Линтеры и автоформатер (flake8, black)
- CI/CD, покрытие тестами

## Технологии 📝

- FastAPI — основной backend (REST API, OpenAPI docs)
- PostgreSQL — хранение пользователей, задач, файлов
- SQLAlchemy — ORM
- Alembic — миграции
- Redis — брокер для Celery
- Celery — фоновые задачи (обработка изображений)
- pytest, httpx — тесты
- poetry — управление зависимостями
- flake8, black — линтеры и автоформатер
- Docker — для локального запуска и деплоя

## Быстрый старт🚀

```bash
git clone https://github.com/Maxim-Proskurin/ImagiQueue.git
cd ImagiQueue
cp .env.example .env
docker-compose up --build
```

### Тесты

```bash
docker-compose exec backend pytest --cov=app
```

### Структура проекта (чек-лист)

- [✅] app/
- [⌛] api/           — Роуты FastAPI
- [⌛] core/          — Настройки, конфиги
- [⌛] models/        — SQLAlchemy модели
- [⌛] schemas/       — Pydantic схемы
- [⌛] services/      — Логика обработки
- [⌛] tasks/         — Celery задачи
- [⌛] main.py        — Точка входа FastAPI
- [✅] alembic/       — Миграции
- [⌛] tests/         — Тесты (pytest, httpx)
- [⌛] docker-compose.yml
- [⌛] Dockerfile
- [✅] pyproject.toml
- [✅] README.md

### Примеры запросов

- Регистрация: POST /auth/register
- Логин: POST /auth/login
- Загрузка изображения: POST /images/upload
- Статус задачи: GET /tasks/{task_id}
- Скачать файл: GET /files/{file_id}/download
- История задач: GET /tasks/history
  