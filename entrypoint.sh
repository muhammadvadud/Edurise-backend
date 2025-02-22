#!/bin/bash
python3 manage.py collectstatic --noinput
python3 manage.py migrate --noinput

poetry run gunicorn app.wsgi:application -b 0.0.0.0:8008 --workers 2

exit $?