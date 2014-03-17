# coding: utf-8

#############################################################################################################
# Константы описывают тип фильма
APP_FILM_FULL_FILM = 'FULL_FILM'
APP_FILM_SERIAL    = 'SERIAL'
APP_PERSON_ACTOR ='actor'
APP_PERSON_PRODUCER ='producer'
APP_PERSON_DIRECTOR = 'director'

APP_FILM_FILM_TYPES = (
    (APP_FILM_FULL_FILM, u'Полнометражный фильм'),
    (APP_FILM_SERIAL, u'Сериал'),
)


APP_FILM_TYPE_ADDITIONAL_MATERIAL = (
    ('POSTER', u'Постер'),
    ('TRAILER', u'Трейлер')
)


APP_FILM_PERSON_TYPES = (
    (APP_PERSON_ACTOR, u'Актер'),
    (APP_PERSON_PRODUCER, u'Продюсер'),
    (APP_PERSON_DIRECTOR, u'Режиссер'),
)
