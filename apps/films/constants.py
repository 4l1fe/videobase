# coding: utf-8

import os
from videobase.settings import STATIC_PATH

#############################################################################################################
APP_PERSON_PHOTO_DIR = os.path.join('upload', 'persons')

#############################################################################################################
APP_FILM_FULL_FILM = 'FULL_FILM'
APP_FILM_SERIAL    = 'SERIAL'

APP_FILM_FILM_TYPES = (
    (APP_FILM_FULL_FILM, u'Полнометражный фильм'),
    (APP_FILM_SERIAL, u'Сериал'),
)

#############################################################################################################
APP_FILM_TYPE_ADDITIONAL_MATERIAL_POSTER = 'POSTER'
APP_FILM_TYPE_ADDITIONAL_MATERIAL_TRAILER = 'TRAILER'

APP_FILM_TYPE_ADDITIONAL_MATERIAL = (
    (APP_FILM_TYPE_ADDITIONAL_MATERIAL_POSTER, u'Постер'),
    (APP_FILM_TYPE_ADDITIONAL_MATERIAL_TRAILER, u'Трейлер')
)

#############################################################################################################
APP_PERSON_ACTOR ='actor'
APP_PERSON_PRODUCER ='producer'
APP_PERSON_DIRECTOR = 'director'

APP_FILM_PERSON_TYPES = (
    (APP_PERSON_ACTOR, u'Актер'),
    (APP_PERSON_PRODUCER, u'Продюсер'),
    (APP_PERSON_DIRECTOR, u'Режиссер'),
)

APP_FILM_CRAWLER_LIMIT = 10
APP_FILM_CRAWLER_DELAY = 10

