## Проект "SPA Веб-приложение на Django, для онлайн-обучения"

## Цели проекта
+ Создания бэкенд-сервера, который возвращает клиенту JSON-структуры с помощью django

## Используются следующие зависимости:

- poetry add django
- poetry init
- pathlib
- poetry add --group lint flake8 black mypy isort 
- ipython
- Pillow
- python-dotenv
- psycopg2-binary
- poetry add djangorestframework


## Использование:
+ Создан проект drf_online_learning
+ Зарегистрировано приложение  materials, users
+ Созданы модели Course, Lesson, User 
+ Описан CRUD для модели Course использую ViewSet
+ Реализован CRUD для модели Lesson с помощью Generic-классов
+ Добавлен эндпоинт для редактирования профиля любого пользователя на основе использования: Viewset
+ Для работы контроллеров написаны простейшие сериализаторы для каждой модели
+ Сервер запускается с помощью команды python manage.py runserver
+ Сервер останавливается командой CTRL+C


## Документация:
Дополнительную информацию о структуре проекта будет позже.

## Команда проекта:
+ **Юлия Самойлова** - Python-разработчик 
+ **Команда SkyPro**