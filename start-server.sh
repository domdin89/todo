#!/usr/bin/env bash
# start-server.sh
# python3 manage.py runserver

python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic
#gunicorn project.wsgi --bind 0.0.0.0:80 --max-requests 1000 --error-logfile error.log
gunicorn todo.wsgi --bind 0.0.0.0:80 \
  --timeout 600 \
  --workers 4 \
  --max-requests 1000 \
  --error-logfile error.log \
