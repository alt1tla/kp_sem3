# Укажите базовый образ
FROM python:3.10

# Установите рабочую директорию
WORKDIR /app

# Скопируйте файл зависимостей и установите их
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Скопируйте проект в контейнер
COPY . /app/

# Соберите статические файлы
RUN python manage.py collectstatic --noinput

# Укажите порт для работы приложения
EXPOSE 8000

# Запустите сервер
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
