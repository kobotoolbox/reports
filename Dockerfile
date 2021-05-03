FROM kobotoolbox/reports_base

###############
# koboreports #
###############

# Freshen dependencies in case they've changed since the base
# image was built
COPY environment.yml /app/
COPY jsapp/package.json jsapp/package-lock.json /app/jsapp/
RUN conda env update --prune
RUN cd jsapp && npm install

# Include all remaining source files except for jsapp/node_modules, which might
# be peculiar to a developer's host environment
COPY . /tmp/app/
RUN (test \! -e /tmp/app/jsapp/node_modules || rm -r /tmp/app/jsapp/node_modules) && \
    (shopt -s dotglob && cp -a /tmp/app/* /app/ && rm -r /tmp/app)

# Build the front end
RUN cd jsapp && npm run build

# Run Python unit tests
RUN source activate koboreports && \
    SECRET_KEY=bogus KPI_API_KEY=bogus ALLOWED_HOSTS=bogus python manage.py test --noinput

# Persistent storage of uploaded XLSForms!
VOLUME ["/app/media"]

# As of Dokku 0.5.0, no ports should be `EXPOSE`d; see
# http://dokku.viewdocs.io/dokku/deployment/methods/dockerfiles/#exposed-ports
CMD ./run.sh # calls `manage.py migrate` and `collectstatic`
