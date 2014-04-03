# coding: utf-8

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
from ConfigParser import RawConfigParser


BASE_PATH = os.path.dirname(__file__)
BASE_DIR = os.path.dirname(BASE_PATH)

#sys.path.insert(0, os.path.join(BASE_PATH, 'apps'))

STATIC_PATH = os.path.join(BASE_PATH, '..', 'static')
CONFIGS_PATH = os.path.join(BASE_PATH, '..', 'configs')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '7-dsc0--i_ej94w9as#-5p_5a)ql*9o80v1rs9krx!_-9%^b5$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*',]

ACCOUNT_ACTIVATION_DAYS = 2

#AUTH_USER_MODEL = 'users.Users'

AUTH_USER_EMAIL_UNIQUE = True

EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = 'info@aasym.com'

# Application definition
INSTALLED_APPS = (
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'registration',
    'south',
    'tastypie',
    'csvimport',
    'apps.users',
    'apps.robots',
    'apps.films',
    'apps.contents',
    'crawler',\
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'utils.middlewares.local_thread.ThreadLocals',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
)

ROOT_URLCONF = 'videobase.urls'

WSGI_APPLICATION = 'videobase.wsgi.application'

# Database
dbconf = RawConfigParser()
dbconf.read(CONFIGS_PATH + '/db.ini')


if 'test' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'videobase_test',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE':   dbconf.get('database', 'DATABASE_ENGINE'),
            'HOST':     dbconf.get('database', 'DATABASE_HOST'),
            'NAME':     dbconf.get('database', 'DATABASE_NAME'),
            'USER':     dbconf.get('database', 'DATABASE_USER'),
            'PASSWORD': dbconf.get('database', 'DATABASE_PASSWORD'),
            'PORT':     dbconf.get('database', 'DATABASE_PORT')
        }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

MEDIA_ROOT = os.path.abspath(BASE_PATH + '/../static')
MEDIA_URL = '/static/'

STATIC_URL = '/production/static/'
STATIC_ROOT = os.path.join('/var/www/')

SITE_ID = 1
