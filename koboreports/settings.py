import os
import dj_database_url

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
THIS_DIR = os.path.dirname(__file__)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'secret')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', True)
TEMPLATE_DEBUG = os.environ.get('TEMPLATE_DEBUG', DEBUG)
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')


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

# https://devcenter.heroku.com/articles/django-assets
STATIC_ROOT = 'static'
STATIC_URL = '/static/'
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

STATICFILES_DIRS = (
    os.path.join(THIS_DIR, 'static'),
)

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
    'reporter.kobo_backend.KoboOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

# START: Settings for python-social-auth
LOGIN_URL = '/login/kobo-oauth2/'
SOCIAL_AUTH_URL_NAMESPACE = 'social'

SOCIAL_AUTH_KOBO_OAUTH2_KEY = 'myclientid'
SOCIAL_AUTH_KOBO_OAUTH2_SECRET = 'mysecretid'
# Don't prompt for authorization if we already have it.
# http://django-oauth-toolkit.readthedocs.org/en/latest/advanced_topics.html#skip-authorization-form
SOCIAL_AUTH_KOBO_OAUTH2_AUTH_EXTRA_ARGUMENTS = {'approval_prompt': 'auto'}
OAUTH2_AUTHORIZATION_URL = os.environ.get(
    'OAUTH2_AUTHORIZATION_URL',
    'https://kf.kobotoolbox.org/forms/o/authorize/'
)
OAUTH2_ACCESS_TOKEN_URL = os.environ.get(
    'OAUTH2_ACCESS_TOKEN_URL',
    'https://kf.kobotoolbox.org/forms/o/token/'
)

KC_URL = 'https://kc.kobotoolbox.org'


# Enable SNI support (see
# http://urllib3.readthedocs.org/en/latest/security.html#openssl-pyopenssl)
import urllib3.contrib.pyopenssl
urllib3.contrib.pyopenssl.inject_into_urllib3()

# END: Settings for python-social-auth

MEDIA_ROOT = 'media'
