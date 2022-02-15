#!/bin/bash

while ! nc -z db 5432; do
    sleep 0.1
done

echo "PostgreSQL started"

python manage.py db migrate

python manage.py db upgrade

python manage.py run -h 0.0.0.0 -p 8000
