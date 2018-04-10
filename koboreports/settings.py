import os
import json
import dj_database_url
from distutils.util import strtobool

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
THIS_DIR = os.path.dirname(__file__)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'secret')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(strtobool(os.environ.get('DEBUG', 'True')))
TEMPLATE_DEBUG = os.environ.get('TEMPLATE_DEBUG', DEBUG)
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')

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
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django.contrib.sites',
    'social.apps.django_app.default',
    'private_storage',
    'reporter',
    'equitytool',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social.apps.django_app.middleware.SocialAuthExceptionMiddleware',
)

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
            "django.contrib.auth.context_processors.auth",
            "django.template.context_processors.debug",
            "django.template.context_processors.i18n",
            "django.template.context_processors.media",
            "django.template.context_processors.request",
            "django.template.context_processors.static",
            "django.template.context_processors.tz",
            "django.contrib.messages.context_processors.messages",
            'social.apps.django_app.context_processors.backends',
            'social.apps.django_app.context_processors.login_redirect',
        )
    }
}]

LOGIN_REDIRECT_URL = '/'

# modify logging settings to see timing data
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'my_formatter': {
            'format': '%(name)s | %(message)s | %(asctime)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'my_formatter',
        },
    },
    'loggers': {
        'TIMING': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
    },
}

AUTHENTICATION_BACKENDS = (
    'reporter.kobo_backend.KoboApiAuthBackend',
    'reporter.kobo_backend.KoboOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

# START: Settings for python-social-auth
#LOGIN_URL = '/login/kobo-oauth2/'
SOCIAL_AUTH_URL_NAMESPACE = 'social'
SOCIAL_AUTH_KOBO_OAUTH2_KEY = os.environ.get('OAUTH_CLIENT_ID', 'myclientid')
SOCIAL_AUTH_KOBO_OAUTH2_SECRET = os.environ.get(
    'OAUTH_CLIENT_SECRET', 'mysecretid')
# Don't prompt for authorization if we already have it.
# http://django-oauth-toolkit.readthedocs.org/en/latest/advanced_topics.html#skip-authorization-form
SOCIAL_AUTH_KOBO_OAUTH2_AUTH_EXTRA_ARGUMENTS = {'approval_prompt': 'auto'}
OAUTH2_AUTHORIZATION_URL = os.environ.get(
    'OAUTH2_AUTHORIZATION_URL',
    'https://kf.kobotoolbox.org/o/authorize/'
)
OAUTH2_ACCESS_TOKEN_URL = os.environ.get(
    'OAUTH2_ACCESS_TOKEN_URL',
    'https://kf.kobotoolbox.org/o/token/'
)

KC_URL = os.environ.get('KOBOCAT_URL', 'https://kc.kobotoolbox.org')

# Enable SNI support (see
# http://urllib3.readthedocs.org/en/latest/security.html#openssl-pyopenssl)
import urllib3.contrib.pyopenssl
urllib3.contrib.pyopenssl.inject_into_urllib3()

# END: Settings for python-social-auth

# KPI now used for user registration and authentication
KPI_URL = os.environ.get('KPI_URL', 'https://kf.kobotoolbox.org/')
KPI_API_KEY = os.environ.get(
    'KPI_API_KEY',
    '8qg3bx7#a2j$o4tuplq==bhdo(4g^d_59ztq&je%pj%tv^!kwgo7&61duo-!'
)
LOGIN_URL = '/api-auth/login/'

''' Sentry configuration '''
if 'RAVEN_DSN' in os.environ:
    import raven
    INSTALLED_APPS = INSTALLED_APPS + (
        'raven.contrib.django.raven_compat',
    )
    RAVEN_CONFIG = {
        'dsn': os.environ['RAVEN_DSN'],
    }
    try:
        RAVEN_CONFIG['release'] = raven.fetch_git_sha(BASE_DIR)
    except raven.exceptions.InvalidGitRepository:
        pass
    # The below is NOT required for Sentry to log unhandled exceptions, but it
    # is necessary for capturing messages sent via the `logging` module.
    # https://docs.getsentry.com/hosted/clients/python/integrations/django/#integration-with-logging
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False, # Was `True` in Sentry documentation
        'root': {
            'level': 'WARNING',
            'handlers': ['sentry'],
        },
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s '
                          '%(process)d %(thread)d %(message)s'
            },
        },
        'handlers': {
            'sentry': {
                'level': 'WARNING',
                'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            }
        },
        'loggers': {
            'django.db.backends': {
                'level': 'ERROR',
                'handlers': ['console'],
                'propagate': False,
            },
            'raven': {
                'level': 'DEBUG',
                'handlers': ['console'],
                'propagate': False,
            },
            'sentry.errors': {
                'level': 'DEBUG',
                'handlers': ['console'],
                'propagate': False,
            },
        },
    }
