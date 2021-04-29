# What is this?

This is a custom application that runs at https://data.equitytool.org. It relies on https://kf.kobotoolbox.org for authentication, form deployment, and submission collection/storage.

## What else is it?

`reports` is a Django project for compiling dynamic reports. It is
built on the R package knitr: http://yihui.name/knitr/.

# Features

Report templates are stored in the database. See
`reporter.models.Template.rmd`.

When rendering a report we can pull data from any URL. See
`reporter.tests.TestRendering.test_url`.

Project is dockerized so it's easy to deploy. See `Dockerfile`.

Mustache tags are supported so we can return a warning message if a
deployment has fewer than 150 responses. See
`reporter.tests.TestRendering.test_warning`.

# Variables passed to Rmd templates

* `rendering__name`: `Rendering.name`, i.e. the user's name for the project
* `form__name`: `Form.name`, e.g. `Tajikistan (DHS 2012)`
* `request__show_urban`: the value of `?show_urban=` in the URL used to request
  the report

# Caveats

* Tables in DOCX exports do not appear properly in LibreOffice: see https://github.com/jgm/pandoc/issues/515

# Development _without_ Dokku

This application requires a working instance of KoBoToolbox to run. See
[kobo-install](https://github.com/kobotoolbox/kobo-install) for instructions
on how to install such an instance.

1. Go to `https://[YOUR KPI DOMAIN]/admin/kpi/authorizedapplication/` (you will
   need to log in as a superuser);
1. Click `Add authorized application`;
1. Name your application and note the randomly-generated key (or enter your
   own);
   1. **NB:** To escape a `$` in the key,
      [double it to `$$`](https://github.com/docker/compose/issues/3427).
1. Click `Save`;
1. Edit `docker-compose.yml` for this `reports` application:
    1. Set the `KPI_API_KEY` environment variable equal to the application key
       generated above;
    1. Set `KPI_URL` to `https://[YOUR KPI DOMAIN]/`;
1. Execute `docker-compose pull`;
1. Execute `docker build -t kobotoolbox/reports_base -f Dockerfile.base .` (this is a slow process);
1. Supplicate before the gods of JavaScript and execute `docker-compose build`;
1. Execute `docker-compose up -d postgres`;
1. Execute `docker-compose logs -f`;
1. Wait for the Postgres container to settle as indicated by the logs;
1. Interrupt (CTRL+C) `docker-compose logs`;
1. Start the application with `docker-compose up -d`;
1. Get a shell inside the application container by running
   `docker-compose exec koboreports bash`;
1. Load some sample `Form`s, if desired:
    1. (Inside the application container) `source activate koboreports`;
    1. `./manage.py loaddata dev/sample-forms.json`;
1. You may want to create a superuser:
    1. (Inside the application container) `source activate koboreports`;
    1. `./manage.py createsuperuser`.
