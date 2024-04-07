#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status
set -x  # all executed commands are printed to the terminal.

export PYTHONUNBUFFERED=0

case "$1" in
    web)
        # Collect static files
        echo "Collect static files"
        poetry run python manage.py collectstatic --noinput

        # Apply database migrations
        echo "Apply database migrations"
        poetry run python manage.py migrate

        # Start server
        echo "Starting server"
        mkdir "/tmp/prom" || true
        export PROMETHEUS_MULTIPROC_DIR=/tmp/prom
        poetry run gunicorn gnezdo_backend.wsgi --preload -b 0.0.0.0:8000 -t60 -w "${CONCURRENCY:-3}"
    ;;
  demo_server)
        poetry run python manage.py collectstatic --noinput
        poetry run python manage.py migrate
        poetry run python manage.py demo_data || true
        poetry run python manage.py runserver --noreload 0.0.0.0:8000

    ;;
    test)
        poetry run coverage run -m pytest && poetry run coverage report && poetry run coverage xml -o reports/coverage.xml
    ;;
    *)
        exec $@
    ;;
esac