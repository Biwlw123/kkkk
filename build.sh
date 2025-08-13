#!/bin/bash
set -e

# Создаем папки для шаблонов
mkdir -p main/templates/main

# Установка зависимостей
pip install -r requirements.txt

# Сбор статики
python manage.py collectstatic --noinput