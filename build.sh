#!/bin/bash
set -e

# Установка зависимостей
pip install -r requirements.txt

# Создание и настройка БД
mkdir -p /tmp/render_db
touch /tmp/render_db/render_db.sqlite3
chmod 644 /tmp/render_db/render_db.sqlite3

# Миграции и статика
python manage.py migrate --noinput
python manage.py collectstatic --noinput