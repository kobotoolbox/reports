import os
import dj_database_url

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

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
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social.apps.django_app.default',
    'reporter',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
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

AUTHENTICATION_BACKENDS = (
    'reporter.kobo_backend.KoboOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

LOGIN_URL = '/login/kobo/'

SOCIAL_AUTH_KOBO_OAUTH_KEY = 'bNxegHZ.a1wUOv.jgiyN!i7tcd3BZRyC0ic=.VNx'
SOCIAL_AUTH_KOBO_OAUTH_SECRET = 'Qswx;HSr9@6-GMGEGeOK9z0DQH;LX0?2-CK:_XDR=z:mQ1rtE1D:X2l;HYmsQVk6_KzO36eYWbszvxpG3.Vt!m3DzpXt5iCl=pujwkG6GpKuuvCFYA4wx15oVPlFb!3s'

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.template.context_processors.debug",
    "django.template.context_processors.i18n",
    "django.template.context_processors.media",
    "django.template.context_processors.static",
    "django.template.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
)
