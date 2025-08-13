#!/bin/bash
set -e

# Установка зависимостей
pip install -r requirements.txt

# Применение миграций
python manage.py migrate --noinput

# Сбор статики
python manage.py collectstatic --noinput

# Создание папок
mkdir -p media staticfiles