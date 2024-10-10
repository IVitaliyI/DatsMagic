# Используем официальный образ Python
FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && apt-get clean

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

# Копируем все остальные файлы проекта (когда они появятся)
COPY . .

# Открываем порт, если приложение будет работать на определенном порту (например, Flask, FastAPI)
EXPOSE 8080

# Команда по умолчанию для запуска приложения (замените на нужную команду, когда проект будет готов)
# Например, для запуска Flask-приложения это может быть: CMD ["python", "app.py"]
# CMD ["ls", "-l"]
CMD python3 ./src/main.py  # Замените на реальную команду позже