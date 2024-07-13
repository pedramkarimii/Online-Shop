#! /usr/bin/env bash

rm -rf db.sqlite3
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser --phone_number 09128355747 --username pedramkarimi --email pedram.9060@gmail.com
python manage.py runserver
