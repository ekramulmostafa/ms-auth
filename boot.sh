#!/bin/sh
source venv/bin/activate
python manage.py db upgrade
uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi:app
