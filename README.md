# SPA Веб-приложение на Django для онлайн-обучения

## 📌 Цели проекта
- Создание бэкенд-сервера с JSON API на Django REST Framework
- Реализация системы онлайн-курсов с платежами и подписками
- Интеграция с Stripe для обработки платежей
- Фоновые задачи через Celery

## 🚀 Быстрый старт (Docker)

### Предварительные требования
- Docker 20.10+
- Docker Compose 2.0+
- Порт 8000 должен быть свободен

### Запуск проекта
bash
# 1. Клонируйте репозиторий (если нужно)
git clone <https://github.com/YuliaSamoylova0803/drf_online_learning>
cd drf_online_learning

# 2. Запустите проект
docker-compose up --build -d

## Проверка работоспособности
bash
### Проверить логи Django
docker-compose logs backend

### Проверить подключение к БД
docker-compose exec db psql -U ${POSTGRES_USER} -d ${POSTGRES_DB} -c "SELECT 1"

### Проверить Redis
docker-compose exec redis redis-cli ping

### Проверить Celery
docker-compose logs celery
Остановка проекта
bash
docker-compose down
## 🛠 Технологический стек
Основные зависимости
- Python 3.13

- Django 4.2

- Django REST Framework

- PostgreSQL

- Redis

- Celery

- Stripe API

## Полный список зависимостей
text
django
djangorestframework
django-filter
djangorestframework-simplejwt
drf-yasg
stripe
forex-python
celery
eventlet
redis
django-celery-beat
psycopg2-binary
python-dotenv
Pillow
## 📚 Функционал
#### Основные возможности
✅ CRUD для курсов и уроков

✅ JWT-аутентификация

✅ Ролевая модель (модераторы/пользователи)

✅ Платежи через Stripe

✅ Подписки на обновления курсов

✅ Фоновые задачи Celery

✅ Документация API (Swagger/Redoc)

✅ Тесты (coverage 88%)

## Модели
+ Course - учебные курсы

+ Lesson - уроки в курсах

+ User - пользователи системы

+ Payment - история платежей

+ Subscribe - подписки на курсы

## 📄 Документация API
После запуска проекта документация доступна по адресам:

Swagger UI: http://localhost:8000/swagger/

ReDoc: http://localhost:8000/redoc/

## 🧪 Тестирование
bash
### Запуск тестов
docker-compose exec backend python manage.py test

### Проверка покрытия
docker-compose exec backend coverage run manage.py test
docker-compose exec backend coverage report
## 👥 Команда проекта
Юлия Самойлова - Python-разработчик

Команда SkyPro - методическая поддержка

## ℹ️ Дополнительная информация
- Все настройки проекта хранятся в .env файле

- Миграции применяются автоматически при запуске контейнера

- Для доступа к админке создайте суперпользователя:


docker-compose exec backend python manage.py createsuperuser