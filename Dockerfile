FROM ubuntu:trusty

###########
# apt-get #
###########

RUN apt-get update && \
    apt-get -y install software-properties-common python-software-properties && \
    add-apt-repository -y ppa:chris-lea/node.js && \
    apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        libgmp10 \
        libpq-dev \
        nodejs \
        texlive-full \
        wget

##########
# pandoc #
##########

# TODO: Remove --no-check-certificate
RUN wget --no-check-certificate https://github.com/jgm/pandoc/releases/download/1.15.0.6/pandoc-1.15.0.6-1-amd64.deb -O pandoc.deb && \
    dpkg -i pandoc.deb && \
    rm pandoc.deb

##############################
# conda install Python and R #
##############################

RUN wget http://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh -O miniconda.sh && \
    chmod +x miniconda.sh && \
    ./miniconda.sh -b && \
    rm miniconda.sh
ENV PATH /root/miniconda2/bin:$PATH
RUN conda update --yes conda

RUN mkdir /app
WORKDIR /app

# https://www.continuum.io/content/conda-data-science
COPY environment.yml /app/
RUN conda env create

# http://stackoverflow.com/a/25423366/3756632
# need this for "source activate" commands
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

# R libraries not available through conda
RUN source activate koboreports && \
    Rscript -e "install.packages('pander', repos='http://cran.rstudio.com/', type='source')" -e "library(pander)"

#############################
# install node dependencies #
#############################

RUN npm install -g grunt-cli
COPY demo/package.json /tmp/package.json
RUN cd /tmp && npm install && mkdir /app/demo && \
    cp -a /tmp/node_modules /app/demo/

###############
# koboreports #
###############

COPY . /app/

WORKDIR /app/demo
RUN grunt build
WORKDIR /app

RUN source activate koboreports && \
    python manage.py test --noinput

# As of Dokku 0.5.0, no ports should be `EXPOSE`d; see
# http://dokku.viewdocs.io/dokku/deployment/methods/dockerfiles/#exposed-ports
CMD ./run.sh # calls `manage.py migrate` and `collectstatic`
