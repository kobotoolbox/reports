FROM kobojohn/kobo-reports-base

################
# install node #
################

RUN apt-get -y install software-properties-common
RUN apt-get -y install python-software-properties
RUN add-apt-repository -y ppa:chris-lea/node.js
RUN apt-get update
RUN apt-get install -y nodejs

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

########################################
# install and build build node project #
########################################


WORKDIR /app/demo
RUN npm install grunt-cli
RUN npm install
RUN grunt build

WORKDIR /app


################################################
# TODO: This is repeated in docker-compose.yml #
################################################

EXPOSE 5000
CMD ["gunicorn", "--bind=0.0.0.0:5000", "--workers=3", "--timeout=300", "koboreports.wsgi"]
