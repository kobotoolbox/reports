FROM kobotoolbox/reports_base

###############
# koboreports #
###############

COPY . /app/

RUN conda env update --prune

WORKDIR /app/jsapp
RUN npm run build
WORKDIR /app

RUN source activate koboreports && \
    python manage.py test --noinput

# Persistent storage of uploaded XLSForms!
VOLUME ["/app/media"]

# As of Dokku 0.5.0, no ports should be `EXPOSE`d; see
# http://dokku.viewdocs.io/dokku/deployment/methods/dockerfiles/#exposed-ports
CMD ./run.sh # calls `manage.py migrate` and `collectstatic`
