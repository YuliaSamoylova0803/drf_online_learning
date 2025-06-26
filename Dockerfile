# Используем официальный slim-образ Python 3.13 (по требованиям вашего проекта)
FROM python:3.13-slim-bookworm

# Устанавливаем системные зависимости (если нужны для psycopg2, Pillow и т.д.)
RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
ENV POETRY_VERSION=1.8.2
ENV POETRY_HOME=/opt/poetry
ENV PATH="$POETRY_HOME/bin:$PATH"

# Устанавливаем Poetry изолированно
RUN pip install "poetry==$POETRY_VERSION"

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файлы зависимостей
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости проекта
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --only main

# Копируем исходный код приложения в контейнер
COPY . .

# Устанавливаем права на запись в media/static
RUN chmod -R 755 /app/media /app/static

# Пробрасываем порт, который будет использовать Django
EXPOSE 8000

# Переменные окружения (лучше перенести в docker-compose или .env)
ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=config.settings

# Команда для запуска приложения
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
