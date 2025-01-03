Last updated: June 16, 2022

# What is this?

`reports` is Django project for compiling dynamic reports using R Markdown and
KoBoToolbox. It is built on the R package knitr: http://yihui.name/knitr/.

This code currently runs on https://data.equitytool.org and relies on
https://kf.kobotoolbox.org for authentication, form deployment, and submission
collection/storage.

# Administrative Reports

To create an administrative report that lists all the users and projects stored
in the database:

1.  Log into https://data.equitytool.org/admin/ as a superuser;
1.  Click "+ Add" next to "Admin stats report tasks";
1.  Click "SAVE";
1.  A screen listing "new report" first as well as previous reports below will
    appear;
1.  Refresh this page every few minutes until "new report" changes into
    "complete report";
1.  Once that happens, click "complete report";
1.  Finally, click "equitytool_admin_stats....zip" (to the right of "Result")
    to download the ZIP file containing the statistics.

# Application Structure (Django Models)

## `equitytool.Form`

An administrator-defined form that regular users can select when they create
new projects. The form is then sent to the regular user's linked KoBoToolbox
account, creating a new project that, in turn, is referenced by a
`reporter.Rendering`

## `reporter.Template`

These R Markdown templates transform collected data from its raw state into
formatted reports (narrative, tables, charts). They are available read-only to
all users, but may only be changed by superusers via the
https://data.equitytool.org/admin/ (Django Admin) interface.

## `reporter.Rendering`

Connects the R Markdown `reporter.Template`s to data collected with
KoBoToolbox. There is one instance of this for each user-created project.

## `reporter.UserExternalApiToken` / User Authentication

This application uses a [special
interface](https://github.com/kobotoolbox/kpi/pull/368/files)
of kf.kobotoolbox.org to create KoBoToolbox users without email confirmation.
Once a user registers in this way, they are then authenticated by sending their
credentials over HTTPS to the KoBoToolbox server (see
`reporter.KoboApiAuthBackend`). If the credentials are correct, KoBoToolbox
returns an API key, which this application then stores in
`reporter.UserExternalApiToken`. That key then authenticates subsequent
requests to deploy forms and retrieve submissions.

There are also local-only users whose passwords (hashed) are stored directly in
this application's database. Superusers are an example of this. These users
have privileges to administer this application but not the connected
KoBoToolbox instance. Local-only users also cannot create data collection
projects as they have no access to KoBoToolbox.

## `equitytool.AdminStatsReportTask`

This model allows [administrative reports](#administrative-reports) to be
generated in the background where they are not subject to the same time limits
as ordinary web application requests.

# R Markdown Templates

Mustache tags are supported so we can return a warning message if a
deployment has fewer than 150 responses. See
`reporter.tests.TestRendering.test_warning`.

## Variables Available in Templates

* `rendering__name`: `Rendering.name`, i.e. the user's name for the project
* `form__name`: `Form.name`, e.g. `Tajikistan (DHS 2012)`
* `request__show_urban`: the value of `?show_urban=` in the URL used to request
  the report

# Known Issues

* Tables in DOCX exports do not appear properly in LibreOffice: see
  https://github.com/jgm/pandoc/issues/515

# Production installation with [Dokku](https://dokku.com/)

For this example, we're using an AWS t3.small EC2 instance, which provides 2
GiB of RAM, along with a 40 GiB EBS root volume. It is running Ubuntu 20.04.

1. Due to the limited amount of RAM, add a 5 GiB swap file:
    ```
    sudo fallocate --length 5G /swapfile
    sudo mkswap /swapfile
    sudo chmod 600 /swapfile
    ```
    Add the following to `/etc/fstab` to enable swap at each boot:
    ```
    /swapfile none swap sw 0 0
    ```
    Enable the swap now:
    ```
    sudo swapon -a
    ```
1. Install Dokku:
    ```
    wget https://raw.githubusercontent.com/dokku/dokku/v0.24.7/bootstrap.sh
    sudo DOKKU_TAG=v0.24.7 bash bootstrap.sh
    sudo reboot
    ```
1. Create the Dokku application:
    ```
    dokku apps:create data.equitytool.org
    ```
1. Configure the new application:
    ```
    dokku config:set data.equitytool.org ALLOWED_HOSTS='data.equitytool.org'
    dokku config:set data.equitytool.org SECRET_KEY='[your randomly-generated Django secret key]'
    # Optional Python exception logging
    dokku config:set data.equitytool.org RAVEN_DSN='[your Sentry DSN]'
    ```
    Connect the application to an instance of KoBoToolbox; see [Development
    _without_ Dokku](#development-without-dokku) for more information:
    ```
    dokku config:set data.equitytool.org KPI_URL='https://kf.kobotoolbox.org'
    dokku config:set data.equitytool.org KPI_API_KEY='[your kpi authorized application key]'
    ```
1. Enable TLS (HTTPS):
    ```
    dokku letsencrypt:enable data.equitytool.org
    ```
1. Enable automatic renewal of TLS certificates:
    ```
    dokku letsencrypt:cron-job --add
    ```
3. Install Postgres and link it with the new application:
    ```
    sudo dokku plugin:install https://github.com/dokku/dokku-postgres.git
    dokku postgres:create reports
    dokku postgres:link reports data.equitytool.org
    ```
1. Add persistent storage for media uploads:
    ```
    dokku storage:mount data.equitytool.org /var/lib/dokku/data/storage/data.equitytool.org:/app/media
    ```
1. Follow the [Dokku
   documentation](https://dokku.com/docs/deployment/application-deployment/#deploy-the-app)
   to deploy the application code from your local machine to this new server
   using `git push`. This relies on the [base image](Dockerfile.base) having
   already been built and pushed to [Docker
   Hub](https://hub.docker.com/r/kobotoolbox/reports_base/tags?page=1&ordering=last_updated)
   by [GitHub Actions](.github/workflows/docker-hub.yml). You must make a new
   [release](https://github.com/kobotoolbox/reports/releases) (or push a new
   tag) to trigger building of the base image. Reducing the size of this base
   image (currently over 4 GiB) would be a nice improvement.

## Deploying an upgrade
1. Make sure the `master` branch on GitHub has been updated with the code you
   want to deploy.
1. Create a new [release](https://github.com/kobotoolbox/reports/releases) (or
   push a new tag) from the tip of `master` to trigger building of the base
   image by [GitHub Actions](.github/workflows/docker-hub.yml).
1. Wait for the build to complete. Verify that the base image for your new
   release is present on [Docker
   Hub](https://hub.docker.com/r/kobotoolbox/reports_base/tags?page=1&ordering=last_updated).
1. Make sure your public SSH key has been added to `authorized_keys` on the
   production server.
1. Use `dokku ssh-keys:list` to verify that your SSH key is added to dokku.
    * If the SSH key needs to be added, copy the `.pub` file on to the server
    and run `dokku ssh-keys:add <keyname> <path/to/key>`
1. Create a new Git remote in your _local_ copy of this repository, unless
   you've already set this up:
    ```
    git remote add PRODUCTION dokku@data.equitytool.org:data.equitytool.org
    ```
1. Make sure the `master` branch in your _local_ repository has been updated
   with the code you want to deploy.
1. Deploy by pushing to the `PRODUCTION` remote:
    ```
    git push PRODUCTION master
    ```
1. Once you're satisfied with the deployment, you may want to prune unused
   Docker resources to save disk space:
    ```
    docker system prune -a
    ```

# Development _without_ Dokku

This application requires a working instance of KoBoToolbox to run. See
[kobo-install](https://github.com/kobotoolbox/kobo-install) for instructions
on how to install such an instance.

1. Go to `https://[YOUR KPI DOMAIN]/admin/kpi/authorizedapplication/` (you will
   need to log in as a superuser);
1. Click `Add authorized application`;
1. Name your application and note the randomly-generated key (or enter your
   own);
    - **NB:** To escape a `$` in the key, [double it to
      `$$`](https://github.com/docker/compose/issues/3427).
1. Click `Save`;
1. Edit `docker-compose.yml` for this `reports` application:
    1. Set the `KPI_API_KEY` environment variable equal to the application key
       generated above;
    1. Set `KPI_URL` to `https://[YOUR KPI DOMAIN]/`;
        * If you are using a locally-hosted KoBoToolbox instance, you may need
          to configure `extra_hosts` as well.
    1. Set `ALLOWED_HOSTS` to match the hostname of your `reports` instance;
       see https://docs.djangoproject.com/en/3.2/ref/settings/#allowed-hosts.
1. Execute `docker compose pull`;
1. Execute `docker build -t kobotoolbox/reports_base -f Dockerfile.base .`
   (this is a slow process);
1. Execute `docker compose build`;
   - **WARNING:** This builds a Docker image using the latest front-end code in
     your source tree, **BUT** the static files and Node dependencies built
     into the Docker image will be shadowed by the `./:/app` volume in
     `docker-compose.yml`. You must run `npm install` and `npm run build` (or
     `npm run dev`) _additionally_, or else the application will run with stale
     code.
1. Execute `docker compose up -d postgres`;
1. Execute `docker compose logs -f`;
1. Wait for the Postgres container to settle as indicated by the logs;
1. Interrupt (CTRL+C) `docker compose logs`;
1. Start the web application with `docker compose up -d`;
1. Get a shell inside the application container by running
   `docker compose exec koboreports bash`;
1. If desired, load some sample `Form`s into the database:
    ```
    # Inside the application container
    source activate koboreports
    ./manage.py loaddata dev/sample-forms.json
    ```
1. To access the Django Admin interface, you'll need a superuser account.
   Create one now:
    ```
    # Inside the application container
    source activate koboreports
    ./manage.py createsuperuser
    ```
1. Build the front-end files:
    1. On your host computer (not inside a Docker container), enter the `jsapp`
       directory within your source tree;
        * (Your source tree is mounted inside the Docker container by the
          `./:/app` volume in `docker-compose.yml`)
    1. Use [nvm](https://github.com/nvm-sh/nvm) or similar to run the same
       version of Node as specified in
       [`Dockerfile.base`](./Dockerfile.base#L1);
    1. Execute `npm install`;
    1. If you plan to do front-end development, execute `npm run dev`, which
       will watch your code for changes and reload as needed.
       * **If you do this,** you must visit the application at
         http://localhost:8080/. Accessing port 5000 will use stale front-end
         code.
    1. If you do not plan to touch front-end code, execute `npm run build` to
       rebuild the front-end static files one time only. **You must do this at
       least once** after switching branches or changing front-end
       dependencies, even if you do not edit any front-end code yourself.
1. Access the application in a browser:
    - If you are **not** working on front-end code and have used only `npm run
      build`, access the application at http://localhost:5000/.
    - If you **are** modifying front-end code and executed `npm run dev`, you
      must access the application at http://localhost:8080/. Port 5000 will
      appear to work, but it will serve stale front-end code.
