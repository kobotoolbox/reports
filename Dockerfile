FROM rocker/hadleyverse:latest

RUN mkdir /app
WORKDIR /app
ADD . /app

RUN wget http://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh -O miniconda.sh
RUN chmod +x miniconda.sh
RUN ./miniconda.sh -b
ENV PATH /root/miniconda/bin:$PATH
RUN conda update --yes conda
RUN conda install --yes --file conda-requirements.txt
RUN pip install -r requirements.txt

RUN python manage.py syncdb --noinput
# RUN python manage.py migrate --noinput
RUN python manage.py collectstatic --noinput

EXPOSE 5000
CMD gunicorn --bind 0.0.0.0:5000 koboreports.wsgi
