FROM kobojohn/kobo-reports-base

##########
# Python #
##########

RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt

###############
# koboreports #
###############

COPY . /app

RUN python manage.py test --noinput

#############################
# database and static files #
#############################

RUN python manage.py migrate --noinput && \
    python manage.py collectstatic --noinput

################################################
# TODO: This is repeated in docker-compose.yml #
################################################

EXPOSE 5000
CMD ["gunicorn", "--bind=0.0.0.0:5000", "--workers=3", "--timeout=300", "koboreports.wsgi"]
