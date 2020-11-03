# What is this?

This is a custom application that runs at https://data.equitytool.org. It relies on https://kf.kobotoolbox.org for authentication, form deployment, and submission collection/storage.

## What else is it?

`reports` is a Django project for compiling dynamic reports. It is
built on the R package [knitr][knitr].

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


# Development _without_ Dokku

This application requires a working instance of KoBoToolbox to run. See
[kobo-docker](https://github.com/kobotoolbox/kobo-docker) for instructions
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
    1. Set `KPI_URL` to `https://[YOUR KPI DOMAIN]/` (must end with a `/`);
    1. Set `KOBOCAT_URL` to `https://[YOUR KOBOCAT DOMAIN]` (must **not** end
       with a slash!);
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
1. Set the domain for the Django sites framework to match the hostname
   (or IP address) of your development machine:
    1. (Inside the application container) `source activate koboreports`;
    1. `./manage.py shell`;
        1. `from django.contrib.sites.models import *`;
        1. `s = Site.objects.first()`;
        1. `s.domain = s.name = 'your.reports.domain'` (include `:port` if
           necessary);
        1. `s.save()`;
        1. `exit()`;
1. Load some sample `Form`s, if desired:
    1. (Inside the application container) `source activate koboreports`;
    1. `./manage.py loaddata dev/sample-forms.json`;
1. You may want to create a superuser:
    1. (Inside the application container) `source activate koboreports`;
    1. `./manage.py createsuperuser`.

# Backburner

On each compilation of a report, it would be nice to save the
corresponding CSV file. That way when the report is recompiled we can
pull only the new / updated data from the API to get the latest
data. I'm not going to worry about setting this up right now, but I'll
keep it in mind in my design decisions.

I am going to ignore different user roles for the moment.  It seems
like there is a large NGO that wants to write reports, and then there
are satellite offices collecting data that will want to view the
reports. For the moment I'm not going to worry too much about
supporting different users and groups.

We will want to share sessions with the other kobo projects on the
server, this will allow users to log in once.

# My Notes

Right now I am deploying this web application using [dokku][dokku]. To
see an instance of this application running go to
[koboreports][koboreports].

Here's how I set up an admin account using dokku:

1.  SSH into AWS server.
2.  Find name of the docker container that is running the application
    using `docker ps`.
3.  Open a bash terminal inside that docker container:

        docker exec -it {{ container_name }} bash

4.  Use django's management command to create a super user:

        python manage.py createsuperuser

One thing to keep in mind when deploying with dokku is every time you
deploy, a new docker container is built. If you are using sqlite to
store data inside a container that data will be lost when you redeploy
the application. I am using postgres to persist data across
deployments.

[knitr]: http://yihui.name/knitr/
[dokku]: http://progrium.viewdocs.io/dokku/
[koboreports]: http://koboreports.hbs-rcs.org/
