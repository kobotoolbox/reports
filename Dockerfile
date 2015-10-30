FROM ubuntu:trusty

###########
# apt-get #
###########

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    libgmp10 \
    libpq-dev \
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

################
# install node #
################

RUN apt-get -y install software-properties-common
RUN apt-get -y install python-software-properties
RUN add-apt-repository -y ppa:chris-lea/node.js
RUN apt-get update
RUN apt-get install -y nodejs

RUN wget http://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh -O miniconda.sh && \
    chmod +x miniconda.sh && \
    ./miniconda.sh -b && \
    rm miniconda.sh
ENV PATH /root/miniconda/bin:$PATH
RUN conda update --yes conda

# pyopenssl fails to run in docker when installed by pip
RUN conda install pyopenssl==0.15.1
RUN mkdir /app
WORKDIR /app/

# https://www.continuum.io/content/conda-data-science
COPY environment.yml /app/
RUN conda env create

# http://stackoverflow.com/a/25423366/3756632
# need this for "source activate" commands
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

# R libraries not available through conda
RUN source activate koboreports && \
    Rscript -e "install.packages('pander', repos='http://cran.rstudio.com/', type='source')" -e "library(pander)"

###############
# koboreports #
###############

COPY . /app/

########################################
# install and build build node project #
########################################


WORKDIR /app/demo
RUN npm install -g grunt-cli
RUN npm install
RUN grunt build

WORKDIR /app


RUN source activate koboreports && \
    python manage.py test --noinput

EXPOSE 5000
CMD ./run.sh
