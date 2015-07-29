FROM rocker/hadleyverse:latest
RUN install2.r --error pander

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y python-pip

RUN mkdir /app
WORKDIR /app
ADD . /app

RUN pip install -r requirements.txt

RUN python manage.py syncdb --noinput
RUN python manage.py migrate --noinput
RUN python manage.py collectstatic --noinput

EXPOSE 5000
CMD gunicorn --bind 0.0.0.0:5000 --workers 3 --timeout 300 koboreports.wsgi
