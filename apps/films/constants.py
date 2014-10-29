# coding: utf-8

import os


#############################################################################################################
APP_PERSON_PHOTO_DIR = os.path.join('upload', 'persons')
APP_FILM_POSTER_DIR = os.path.join('upload', 'filmextras')

#############################################################################################################
APP_FILM_FULL_FILM = u'FULL_FILM'
APP_FILM_SERIAL    = u'SERIAL'

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
APP_PERSON_ACTOR = 'actor'
APP_PERSON_PRODUCER = 'producer'
APP_PERSON_DIRECTOR = 'director'
APP_PERSON_SCRIPTWRITER = 'scriptwriter'

APP_FILM_PERSON_TYPES = (
    (APP_PERSON_ACTOR, u'Актер'),
    (APP_PERSON_PRODUCER, u'Продюсер'),
    (APP_PERSON_DIRECTOR, u'Режиссер'),
    (APP_PERSON_SCRIPTWRITER, u'Сценарист'),
)

APP_FILM_PERSON_TYPES_OUR = (
    ('a', APP_PERSON_ACTOR),
    ('p', APP_PERSON_PRODUCER),
    ('d', APP_PERSON_DIRECTOR),
    ('s', APP_PERSON_SCRIPTWRITER),
    ('all', '')
)

APP_FILM_CRAWLER_LIMIT = 10
APP_FILM_CRAWLER_DELAY = 10

#############################################################################################################
APP_JQUERY_PATH = 'http://code.jquery.com/jquery-1.9.1.js'
APP_FILM_ADMIN_JS_LIBS = ('http://code.jquery.com/jquery-1.9.1.js',
                          'http://cdnjs.cloudflare.com/ajax/libs/camanjs/3.3.0/caman.full.min.js',
                          'http://code.jquery.com/ui/1.10.4/jquery-ui.js',
                          '/static/jcrop/js/jquery.Jcrop.js',
                          '/static/resize.js',
                          '/static/links.js'
                      )

APP_FILM_ADMIN_CSS = ('http://code.jquery.com/ui/1.10.4/themes/smoothness/jquery-ui.css',)


#############################################################################################################
APP_USERFILM_STATUS_UNDEF = 0
APP_USERFILM_STATUS_NOT_WATCH = 1
APP_USERFILM_STATUS_PLAYLIST = 2

APP_USERFILM_STATUS = (
    (APP_USERFILM_STATUS_UNDEF, u'Не определено'),
    (APP_USERFILM_STATUS_NOT_WATCH, u'Не буду смотреть'),
    (APP_USERFILM_STATUS_PLAYLIST, u'В плейлисте'),
)

#############################################################################################################
APP_USERFILM_SUBS_FALSE = 0
APP_USERFILM_SUBS_TRUE = 1

APP_USERFILM_SUBS = (
    (APP_USERFILM_SUBS_FALSE, u'Не подписан'),
    (APP_USERFILM_SUBS_TRUE, u'Подписан'),
)

#############################################################################################################
APP_PERSONFILM_SUBS_FALSE = 0
APP_PERSONFILM_SUBS_TRUE = 1

APP_PERSONFILM_SUBS = (
    (APP_PERSONFILM_SUBS_FALSE, u'Не подписан'),
    (APP_PERSONFILM_SUBS_TRUE, u'Подписан'),
)

#############################################################################################################
APP_FILMS_API_DEFAULT_PAGE = 1
APP_FILMS_API_DEFAULT_PER_PAGE = 12

#############################################################################################################
APP_COMMENTS_API_DEFAULT_PAGE = 1
APP_COMMENTS_API_DEFAULT_PER_PAGE = 10

#############################################################################################################
APP_FILMS_EXTRAS_POSTER_HOST = 'http://vsevi.ru/static/'


APP_FILMS_WEEK_SUB_EMAIL = u'Eженедельная рассылка ВсеВи'
APP_FILMS_PERSON_SUB_EMAIL = u'Персональная рассылка ВсеВи'
