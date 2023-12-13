#!/bin/bash

export PATH="/opt/dart-sass:$PATH"

python manage.py migrate
python manage.py collectstatic --no-input

python manage.py createsuperuser --noinput
python manage.py runserver 0.0.0.0:8000

# gunicorn --config gunicorn-cfg.py core.wsgi