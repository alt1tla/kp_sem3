# Указываем базовый образ Python
FROM python:3.11

# Устанавливаем рабочую директорию в контейнере
WORKDIR /game

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в контейнер
COPY . .

# Указываем порт, который будет использоваться
EXPOSE 8000

# Указываем команду для запуска проекта
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
