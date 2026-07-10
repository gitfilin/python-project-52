[![Actions Status](https://github.com/gitfilin/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/gitfilin/python-project-52/actions)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=gitfilin_python-project-52&metric=coverage)](https://sonarcloud.io/summary/new_code?id=gitfilin_python-project-52)

# Task Manager

Task Manager — это веб-приложение для управления задачами.
Пользователи могут создавать задачи, назначать исполнителей, менять статусы и добавлять метки.
Также доступна фильтрация задач по статусу, исполнителю, метке и автору.

Проект разработан на **Python + Django** в рамках обучения на платформе Hexlet.

## Demo

Приложение доступно по адресу:

https://task-manager-hexlet-ay86.onrender.com/

## Возможности

* регистрация и авторизация пользователей
* управление пользователями (создание, редактирование, удаление)
* создание, редактирование и удаление задач
* назначение исполнителя
* статусы задач
* метки (labels) для задач
* фильтрация задач по:

  * статусу
  * исполнителю
  * метке
  * своим задачам
* защита операций авторизацией
* защита от удаления связанных сущностей
* отслеживание ошибок через Rollbar

## Технологии

* Python 3.14
* Django 6.06
* django-filter
* django-bootstrap5
* Bootstrap 5
* Gunicorn
* Whitenoise
* Render
* Rollbar

## Установка и запуск

### 1. Клонирование репозитория

```bash
git clone git@github.com:gitfilin/python-project-52.git
cd python-project-52
```

### 2. Установка зависимостей

Проект использует пакетный менеджер **uv**.

```bash
make install
```

### 3. Создание `.env`

Создайте файл `.env` в корне проекта:

```env
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
ROLLBAR_ACCESS_TOKEN=your_rollbar_token
ROLLBAR_ENVIRONMENT=development
```

### 4. Применение миграций

```bash
make migrate
```

### 5. Запуск приложения

```bash
make start
```

После запуска приложение будет доступно по адресу:

```
http://localhost:8000
```

## Запуск тестов

```bash
uv run python manage.py test
```

## Линтер

```bash
uv run ruff check .
```
