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

ALLOWED_HOSTS = ['*', ]

ACCOUNT_ACTIVATION_DAYS = 2

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
    'south',
    'rest_framework',
    'rest_framework.authtoken',
    'social_auth',
    'csvimport',
    'apps.users',
    'apps.films',
    'apps.contents',
    'apps.robots',
    'crawler',
    'social_auth',
    'djcelery',
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
    # Social
    'social_auth.context_processors.social_auth_by_type_backends',
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates/'),
    os.path.join(BASE_DIR, 'interface/'),
)

ROOT_URLCONF = 'videobase.urls'

WSGI_APPLICATION = 'videobase.wsgi.application'

# Database
dbconf = RawConfigParser()
dbconf.read(CONFIGS_PATH + '/db.ini')


if 'test' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE':   dbconf.get('testbase', 'DATABASE_ENGINE'),
            'HOST':     dbconf.get('testbase', 'DATABASE_HOST'),
            'NAME':     dbconf.get('testbase', 'DATABASE_NAME'),
            'USER':     dbconf.get('testbase', 'DATABASE_USER'),
            'PASSWORD': dbconf.get('testbase', 'DATABASE_PASSWORD'),
            'PORT':     dbconf.get('testbase', 'DATABASE_PORT')
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
        'PREFIX': 'weee:',
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

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.XMLRenderer',
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'apps.users.models.api_session.MultipleTokenAuthentication',
    )
}

LOGIN_REDIRECT_URL = '/'

# Ключи для OAuth2 авторизации
# Vkontakte
VK_APP_ID            = '4296663'
VKONTAKTE_APP_ID     = VK_APP_ID
VK_API_SECRET        = 'JAEQddzkBCm554iGXe6S'
VKONTAKTE_APP_SECRET = VK_API_SECRET
VK_EXTRA_SCOPE = ['notify', 'friends', 'status', 'groups', 'notifications']
# Facebook
FACEBOOK_APP_ID     = '212532105624824'
FACEBOOK_API_SECRET = 'a99fcef38b7054279d73beb4ebb7b6cc'
# Twitter
TWITTER_CONSUMER_KEY    = 'HACuJARrAXJyeHdeD5viHULZR'
TWITTER_CONSUMER_SECRET = 'Ge0k2rKltyPq3ida76IjTbhesZVdIrvckcNPXzJaBU2ouzixut'
# Google+
GOOGLE_OAUTH2_CLIENT_ID     = 'AIzaSyD9C36HCncY0tVWQekEmz5KEarnCzOCCb0'
GOOGLE_OAUTH2_CLIENT_SECRET = ''
# Mail.ru
MAILRU_OAUTH2_APP_KEY = '719516'
MAILRU_OAUTH2_CLIENT_KEY = '4daa3ed8bef5be08ebd7e25ff5ae806a'
MAILRU_OAUTH2_CLIENT_SECRET = '8cc7bb50e5b93663774e6584a1251d79'

SOCIAL_AUTH_CREATE_USERS = True

# Backends for social auth
AUTHENTICATION_BACKENDS = (
    'social_auth.backends.twitter.TwitterBackend',
    'social_auth.backends.facebook.FacebookBackend',
    'social_auth.backends.contrib.vk.VKOAuth2Backend',
    'social_auth.backends.google.GoogleOAuth2Backend',
    'social_auth.backends.contrib.odnoklassniki.OdnoklassnikiBackend',
    'social_auth.backends.contrib.mailru.MailruBackend',
    'django.contrib.auth.backends.ModelBackend',
    'rest_framework.authentication.TokenAuthentication',
    'apps.users.models.api_session.MultipleTokenAuthentication',
)

# Перечислим pipeline, которые последовательно буду обрабатывать респонс
SOCIAL_AUTH_PIPELINE = (
    # Получает по backend и uid инстансы social_user и user
    'social_auth.backends.pipeline.social.social_auth_user',
    # Получает по user.email инстанс пользователя и заменяет собой тот, который получили выше.
    # Кстати, email выдает только Facebook и GitHub, а Vkontakte и Twitter не выдают
    'social_auth.backends.pipeline.associate.associate_by_email',
    # Пытается собрать правильный username, на основе уже имеющихся данных
    'social_auth.backends.pipeline.user.get_username',
    # Создает нового пользователя, если такого еще нет
    'social_auth.backends.pipeline.user.create_user',
    # Пытается связать аккаунты
    'social_auth.backends.pipeline.social.associate_user',
    # Получает и обновляет social_user.extra_data
    'social_auth.backends.pipeline.social.load_extra_data',
    # Обновляет инстанс user дополнительными данными с бекенда
    'social_auth.backends.pipeline.user.update_user_details'
)

# In minutes
API_SESSION_EXPIRATION_TIME = 15

if not DEBUG:
    INSTALLED_APPS += (
        'django_jenkins',
        'raven.contrib.django.raven_compat',  # may be delete later
    )

    RAVEN_CONFIG = {
        'dsn': 'http://8684bf8b497047d9ac170fd16aefc873:41e89f4666b24f998125370f3d1a1789@sentry.aaysm.com/2'
    }

    JENKINS_TASKS = ('django_jenkins.tasks.run_pylint',
                     'django_jenkins.tasks.run_pep8',
                     'django_jenkins.tasks.run_pyflakes',
                     'django_jenkins.tasks.with_coverage',)

from datetime import timedelta

CELERYBEAT_SCHEDULE = {
    'robot-launch': {
        'task': 'robot_launch',
        'schedule': timedelta(minutes=5),
    },
    'kinopoisk-get_id': {
        'task': 'kinopoisk_get_id',
        'shedule': timedelta(minutes=5),
    },
}

CELERY_TIMEZONE = 'UTC'
