source activate koboreports

python manage.py migrate --noinput
python manage.py collectstatic --noinput

gunicorn --bind=0.0.0.0:5000 --workers=3 --timeout=300 koboreports.wsgi