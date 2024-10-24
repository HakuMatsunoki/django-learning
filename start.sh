#!/bin/bash

echo ">>> make migrations >>>"
python manage.py makemigrations

echo ">>> migrate >>>"
python manage.py migrate

echo ">>> run server >>>"
exec python manage.py runserver 0.0.0.0:8000