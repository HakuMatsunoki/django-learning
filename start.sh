#!/bin/bash

echo ">>> compile translations >>>"
python manage.py compilemessages

echo ">>> run server >>>"
python manage.py runserver 0.0.0.0:8000
