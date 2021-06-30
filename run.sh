#!/bin/bash

# This script should be run inside a Docker container;
# see the `CMD` line in the `Dockerfile`

source activate koboreports

# Do not proceed with startup if these fail
python manage.py migrate --noinput || exit 1
python manage.py collectstatic --noinput || exit 1

# Start the asynchronous task runner for admin report generation
trap 'kill $(jobs -p)' EXIT
python manage.py run_huey --no-periodic || exit 1 &

# Enable Gunicorn auto-reloading if DEBUG=True (case insensitive)
if [ "${DEBUG,,}" == 'true' ]
then
    gunicorn --bind=0.0.0.0:$PORT --workers=3 --timeout=300 --reload koboreports.wsgi
else
    # You must set the NGINX `proxy_read_timeout` to something greater than or
    # equal to the Gunicorn `--timeout` value specified here
    gunicorn --bind=0.0.0.0:$PORT --workers=3 --timeout=300 koboreports.wsgi
fi

