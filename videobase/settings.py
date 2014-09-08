# coding: utf-8
import os
import djcelery

from datetime import timedelta
from ConfigParser import RawConfigParser

###########################################################
# Celery settings
os.environ["CELERY_LOADER"] = "django"
djcelery.setup_loader()

AMQP_HOST = 'localhost'
BROKER_HOST = 'localhost'
BROKER_PORT = 5672
###########################################################

BASE_PATH = os.path.dirname(__file__)
BASE_DIR = os.path.dirname(BASE_PATH)

STATIC_PATH = os.path.join(BASE_PATH, '..', 'static')
CONFIGS_PATH = os.path.join(BASE_PATH, '..', 'configs')
BACKUP_PATH = os.path.join(BASE_PATH, '..', '.backup')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '7-dsc0--i_ej94w9as#-5p_5a)ql*9o80v1rs9krx!_-9%^b5$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*']

ACCOUNT_ACTIVATION_DAYS = 2

AUTH_USER_EMAIL_UNIQUE = True

HTTP_SESSION_TOKEN_TYPE = b'X-MI-SESSION'
HTTP_USER_TOKEN_TYPE = b'X-MI-TOKEN'

STANDART_HTTP_SESSION_TOKEN_HEADER = b'HTTP_{}'.format(HTTP_SESSION_TOKEN_TYPE.replace('-', '_'))
STANDART_HTTP_USER_TOKEN_HEADER = b'HTTP_{}'.format(HTTP_USER_TOKEN_TYPE.replace('-', '_'))

DEFAULT_REST_API_RESPONSE = {}
###########################################################
emailconf = RawConfigParser()
emailconf.read(CONFIGS_PATH + '/email.ini')
EMAIL_HOST = emailconf.get('email', 'EMAIL_HOST')
EMAIL_PORT = emailconf.getint('email', 'EMAIL_PORT')
EMAIL_HOST_USER = emailconf.get('email', 'EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = emailconf.get('email', 'EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = emailconf.getboolean('email', 'EMAIL_USE_TLS')
EMAIL_BACKEND = emailconf.get('email', 'EMAIL_BACKEND')
DEFAULT_FROM_EMAIL = emailconf.get('email', 'DEFAULT_FROM_EMAIL')

###########################################################
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
    'django_nose',
    'treebeard',
    'rest_framework',
    'rest_framework.authtoken',
    'social_auth',
    'csvimport',
    'apps.users',
    'apps.films',
    'apps.contents',
    'apps.robots',
    'apps.rss',
    'apps.git',
    'apps.casts',
    'crawler',
    'social_auth',
    'djcelery',
    'backup_system',
    'data',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'utils.middlewares.AuthTokenMiddleware',
    'utils.middlewares.ThreadLocals',
    'utils.middlewares.ExceptionMiddleware'
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

# Backends for social auth
AUTHENTICATION_BACKENDS = (
    # OAuth
    'social_auth.backends.twitter.TwitterBackend',
    'social_auth.backends.facebook.FacebookBackend',
    'social_auth.backends.contrib.vk.VKOAuth2Backend',
    'social_auth.backends.google.GoogleOAuth2Backend',

    # Django
    'django.contrib.auth.backends.ModelBackend',
)

###########################################################
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
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'apps.users.backends.SessionTokenAuthentication',
        'apps.users.backends.UserTokenAuthentication',
    )
}

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

LOGIN_URL = '/login'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/tokenize/'
LOGIN_ERROR_URL = '/'

###########################################################
# Ключи для OAuth2 авторизации
# Vkontakte
VK_APP_ID            = '4296663'
VKONTAKTE_APP_ID     = VK_APP_ID
VK_API_SECRET        = 'JAEQddzkBCm554iGXe6S'
VKONTAKTE_APP_SECRET = VK_API_SECRET

# Facebook
FACEBOOK_APP_ID     = '212532105624824'
FACEBOOK_API_SECRET = 'a99fcef38b7054279d73beb4ebb7b6cc'
FACEBOOK_EXTENDED_PERMISSIONS = ['email', ]

# Twitter
TWITTER_CONSUMER_KEY    = 'HACuJARrAXJyeHdeD5viHULZR'
TWITTER_CONSUMER_SECRET = 'Ge0k2rKltyPq3ida76IjTbhesZVdIrvckcNPXzJaBU2ouzixut'

# Google+
GOOGLE_OAUTH2_CLIENT_ID     = '729866043170.apps.googleusercontent.com'
GOOGLE_OAUTH2_CLIENT_SECRET = 'Ga91PMNEXi28egLsTUy5Wqhw'

GOOGLE_OAUTH2_USE_UNIQUE_USER_ID = True

SOCIAL_AUTH_CREATE_USERS = True
SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True

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
)


# In minutes
API_SESSION_EXPIRATION_TIME = 15


###########################################################
CELERYBEAT_SCHEDULE = {

    # Launching robots that are described in Robots table.
    #'robot-launch': {
    #    'task': 'robot_launch',
    #    'schedule': timedelta(seconds=10),
    #},

    # Updating ratings from IMDB DB via archive
    'imdb_rating_update_command': {
        'task': 'imdb_rating_update',
        'schedule': timedelta(days=7),
    },
    # Amediateka weekly run
    'amediateka_ru_update': {
        'task': 'amediateka_ru_robot_start',
        'schedule': timedelta(days=7),
    },
    # Viaplay robot weekly run
    'viaplay_ru_robot_start': {
        'task': 'viaplay_ru_robot_start',
        'schedule': timedelta(days=7),
    },
    'kinopoisk-set_poster': {
        'task': 'kinopoisk_set_poster',
        'schedule': timedelta(seconds=10),
    },
    # Updating information about persons using kinopoisk
    'kinopoisk_persons': {
        'task': 'kinopoisk_persons',
        'schedule': timedelta(seconds=10),
    },
    # Checking kinopoisk premiere page
    'kinopoisk_news': {
        'task': 'kinopoisk_news',
        'schedule': timedelta(days=3),
    },
    # Youtube trailers
    'youtube_trailers': {
        'task': 'youtube_trailers_all',
        'schedule': timedelta(days=1),
    },
    # Three tasks that parse information from kinopoisk navigator page
    'kinopoisk_films_daily': {
        'task': 'kinopoisk_films',
        'schedule': timedelta(days=1),
        'args': (3,),
    },
    'kinopoisk_films_weekly': {
        'task': 'kinopoisk_films',
        'schedule': timedelta(days=7),
        'args': (10,),
    },
    'kinopoisk_films_monthly': {
        'task': 'kinopoisk_films',
        'schedule': timedelta(days=31),
        'args': (1100,),
    },
    # Task that periodically requests information from kinopoisk depending on film age
    'kinopoisk_refresh': {
        'task': 'kinopoisk_refresher',
        'schedule': timedelta(days=1),
    },
    # Playfamily XML parser.
    'playfamily_xml': {
        'task': 'playfamily_xml',
        'schedule': timedelta(days=7),
    },
    # Films check and correct
    'film_info_check_and_correct': {
        'task': 'film_info_check_and_correct',
        'schedule': timedelta(days=7),
    },

     # Persons check and correct
    'persons_check_and_correct': {
        'task': 'persons_check_and_correct',
        'schedule': timedelta(days=7),
    },

    # Checking locations for new films weekly
    'age_weighted_robot_launch_task_weekly': {
        'task': 'age_weighted_robot_launch',
        'schedule': timedelta(days=7),
        'args': (1,)
    },
    # Checking locations for aged films monthly
    'age_weighted_robot_launch_task_monthly': {
        'task': 'age_weighted_robot_launch',
        'schedule': timedelta(days=31),
        'args': (3,)
    },

    # Checking locations for aged films yearly
    'age_weighted_robot_launch_task_six_month': {
        'task': 'age_weighted_robot_launch',
        'schedule': timedelta(days=31*6),
        'args': (120,)
    },
    'drugoe_kino_update_schedule': {
        'task': 'drugoe_kino_update',
        'schedule': timedelta(days=7)
    },
    # Refreshing sitemap
    'sitemap_refresh_schedule': {
        'task': 'refresh_sitemap',
        'schedule': timedelta(days=14)
    },
     # Parsing videos from YouTubeMoviesRU
    'parse_you_tube_movies_ru': {
        'task': 'parse_you_tube_movies_ru',
        'schedule': timedelta(days=1)
    },
    # Refreshing consolidate rating
    'consolidate_rating_schedule': {
        'task': 'consolidate_rating',
        'schedule': timedelta(days=1)
    },

    # Send robots statistic to email
    'send_robots_statistic_to_email': {
        'task': 'send_robots_statistic_to_email',
        'schedule': timedelta(days=1)
    },

    # News from now.ru
    'parse_news_from_now_ru': {
        'task': 'parse_news_from_now_ru',
        'schedule': timedelta(hours=12)
    },

    # News from stream.ru
    'parse_news_from_stream_ru': {
        'task': 'parse_news_from_stream_ru',
        'schedule': timedelta(hours=12)
    },

    
}

CELERY_TIMEZONE = 'UTC'
CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']
POSTER_URL_PREFIX = '_260x360'
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

from local_settings import *

if not DEBUG:
    INSTALLED_APPS += (
        'raven.contrib.django.raven_compat',  # may be delete later
    )

    RAVEN_CONFIG = {
        'dsn': 'http://8684bf8b497047d9ac170fd16aefc873:41e89f4666b24f998125370f3d1a1789@sentry.aaysm.com/2'
    }
