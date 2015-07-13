FROM python:2.7

ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app/
RUN pip install -r requirements.txt
ADD . /app/

EXPOSE 5000
CMD gunicorn --bind 0.0.0.0:5000 koboreports.wsgi