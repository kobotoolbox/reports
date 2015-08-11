FROM rocker/hadleyverse:latest

#####################
# extra R libraries #
#####################

RUN install2.r --error pander

####################
# apt-get installs #
####################

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y \
    python-pip \
    python-dev \
    curl

################
# pip installs #
################

RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app/
RUN pip install -r requirements.txt

#############
# copy code #
#############

ADD . /app

########################
# make sure tests pass #
########################

RUN python manage.py test

###########################################
# setup database and collect static files #
###########################################

RUN python manage.py syncdb --noinput
RUN python manage.py migrate --noinput
RUN python manage.py collectstatic --noinput

################################################
# TODO: This is repeated in docker-compose.yml #
################################################

EXPOSE 5000
gunicorn --bind 0.0.0.0:5000 --workers 3 --timeout 300 koboreports.wsgi