source activate koboreports

python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Enable Gunicorn auto-reloading if DEBUG=True (case insensitive)
[ "${DEBUG,,}" == 'true' ] && AUTORELOAD='--reload' || AUTORELOAD=''

# you probably need to set the NGINX `proxy_read_timeout` for `--timeout=300`
# to be of any use
gunicorn --bind=0.0.0.0:$PORT --workers=3 --timeout=300 "$AUTORELOAD" koboreports.wsgi
