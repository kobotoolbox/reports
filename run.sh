python manage.py syncdb --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput

gunicorn --bind 0.0.0.0:5000 koboreports.wsgi
