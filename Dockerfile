FROM ubuntu:trusty

###########
# apt-get #
###########

RUN echo "deb http://cran.rstudio.com/bin/linux/ubuntu trusty/" > /etc/apt/sources.list.d/r.list && \
    gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys E084DAB9 && \
    gpg -a --export E084DAB9 | apt-key add -

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    libgmp10 \
    libpq-dev \
    littler \
    r-base \
    texlive-full \
    wget

##########
# pandoc #
##########

RUN wget https://github.com/jgm/pandoc/releases/download/1.15.0.6/pandoc-1.15.0.6-1-amd64.deb -O pandoc.deb && \
    dpkg -i pandoc.deb && \
    rm pandoc.deb

#####
# R #
#####

RUN echo 'options(repos = list(CRAN = "https://cran.rstudio.com/"), download.file.method = "libcurl")' >> /etc/R/Rprofile.site \
    && echo 'source("/etc/R/Rprofile.site")' >> /etc/littler.r \
    && ln -s /usr/share/doc/littler/examples/install.r /usr/local/bin/install.r \
    && ln -s /usr/share/doc/littler/examples/install2.r /usr/local/bin/install2.r \
    && ln -s /usr/share/doc/littler/examples/installGithub.r /usr/local/bin/installGithub.r \
    && ln -s /usr/share/doc/littler/examples/testInstalled.r /usr/local/bin/testInstalled.r \
    && install.r docopt

RUN install2.r --error \
    RPostgreSQL \
    dplyr \
    ggplot2 \
    knitr \
    pander \
    rmarkdown \
    tidyr \
    whisker

##########
# Python #
##########

RUN wget http://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh -O miniconda.sh && \
    chmod +x miniconda.sh && \
    ./miniconda.sh -b && \
    rm miniconda.sh

ENV PATH /root/miniconda/bin:$PATH

RUN conda update --yes conda && \
    conda install \
        pandas=0.16.2=np19py27_0 \
        pip 

RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt

###############
# koboreports #
###############

COPY . /app

RUN python manage.py test

#############################
# database and static files #
#############################

RUN python manage.py syncdb --noinput && \
    python manage.py migrate --noinput && \
    python manage.py collectstatic --noinput

################################################
# TODO: This is repeated in docker-compose.yml #
################################################

EXPOSE 5000
CMD ["gunicorn", "--bind=0.0.0.0:5000", "--workers=3", "--timeout=300", "koboreports.wsgi"]
