#!/bin/sh
source venv/bin/activate
python manage.py db upgrade
uwsgi --ini uwsgi.ini
