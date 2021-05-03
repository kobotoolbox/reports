import os
import json
import dj_database_url
from distutils.util import strtobool
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
THIS_DIR = os.path.dirname(__file__)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(strtobool(os.environ.get('DEBUG', 'False')))
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')
if not DEBUG and not ''.join(ALLOWED_HOSTS):
    raise ImproperlyConfigured(
        'You must define ALLOWED_HOSTS in your environment when running in '
        'production mode'
    )


# Django doesn't always recognize HTTPS when terminated by Dokku's NGINX proxy
# Allow recognition of HTTPS by reading a header injected by NGINX, e.g.
# to recognize 'X-Forwarded-Proto: https', set
# `SECURE_PROXY_SSL_HEADER=["HTTP_X_FORWARDED_PROTO", "https"]` in the
# environment
if 'SECURE_PROXY_SSL_HEADER' in os.environ:
    SECURE_PROXY_SSL_HEADER = json.loads(os.environ['SECURE_PROXY_SSL_HEADER'])


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'private_storage',
    'reporter',
    'equitytool',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'koboreports.urls'

WSGI_APPLICATION = 'koboreports.wsgi.application'

DATABASES = {
    'default': dj_database_url.config(default='sqlite:///db.sqlite')
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(THIS_DIR, 'static'),
)

PRIVATE_STORAGE_ROOT = os.path.join(BASE_DIR, 'media')
PRIVATE_STORAGE_AUTH_FUNCTION = \
    'private_storage.permissions.allow_staff'


TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [
        os.path.join(THIS_DIR, 'templates'),
    ],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': (
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        )
    }
}]

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = 'https://www.equitytool.org/'

AUTHENTICATION_BACKENDS = (
    'reporter.kobo_backend.KoboApiAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
)

KPI_URL = os.environ.get('KPI_URL', 'https://kf.kobotoolbox.org/')
if KPI_URL and KPI_URL[-1] != '/':
    # Make sure a trailing URL is included
    KPI_URL += '/'

KPI_API_KEY = os.environ.get('KPI_API_KEY')
if not KPI_API_KEY:
    raise ImproperlyConfigured('You must define KPI_API_KEY in your environment')

LOGIN_URL = '/api-auth/login/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


''' Sentry error-logging configuration '''

try:
    sentry_dsn = os.environ['SENTRY_DSN']
except KeyError:
    try:
        sentry_dsn = os.environ['RAVEN_DSN']
    except KeyError:
        sentry_dsn = None
if sentry_dsn:
    # https://docs.sentry.io/platforms/python/guides/django/
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    sentry_sdk.init(
        dsn=sentry_dsn,
        integrations=[DjangoIntegration()],
        traces_sample_rate=1.0,
        send_default_pii=True,
    )
