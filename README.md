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
