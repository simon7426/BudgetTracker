#!/bin/bash

while ! nc -z 36.255.69.121 5432; do
    sleep 0.1
done

echo "PostgreSQL started"

python manage.py run -p 8000