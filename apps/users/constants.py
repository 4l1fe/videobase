# coding: utf-8

import os
from videobase.settings import STATIC_PATH

#############################################################################################################
APP_USER_PIC_DIR = os.path.join('upload', 'users', 'user_pic')

#############################################################################################################
APP_USER_REL_TYPE_FRIENDS              = 'f'
APP_USER_REL_TYPE_SEND_NOT_RECEIVED    = 's'
APP_USER_REL_TYPE_ACCEPRED_NOT_ADOPTED = 'r'
APP_USER_REL_TYPE_NONE                 = 'null'

APP_USER_REL_TYPES = (
    (APP_USER_REL_TYPE_FRIENDS, 'Друзья'),
    (APP_USER_REL_TYPE_SEND_NOT_RECEIVED, 'Заявка отправлена, но не принята'),
    (APP_USER_REL_TYPE_ACCEPRED_NOT_ADOPTED, 'Заявка получена, но не принята'),
)

#############################################################################################################
APP_USER_ACTIVE   = 0
APP_USER_INACTIVE = 1

APP_USER_STATUS = (
    (APP_USER_ACTIVE,  u'Активный'),
    (APP_USER_INACTIVE, u'Заблокирован')
)

#############################################################################################################
APP_USER_PIC_TYPES = (
    ('SOCIAL', 'Из социальных сетей'),
    ('LOCAL', 'Сохранные изображения')
)

APP_SUBJECT_TO_RESTORE_PASSWORD = u'Востановление пароля'
APP_SUBJECT_TO_CONFIRM_REGISTER = u'Подтверждение регистрации'
APP_SUBJECT_TO_NOTIFICATION_FILM = u'Появился фильм'
APP_SUBJECT_TO_NOTIFICATION_PERSON = u'Новый фильм у персоны'

APP_USERS_API_DEFAULT_PER_PAGE = 10
APP_USERS_API_DEFAULT_PAGE = 1

#############################################################################################################
FILM_RATE = 'film-r'
FILM_SUBSCRIBE = 'film-s'
FILM_NOTWATCH = 'film-nw'
FILM_COMMENT = 'film-c'
FILM_O = 'film-o'
PERSON_SUBSCRIBE = 'pers-s'
PERSON_O = 'pers=o'
USER_ASK = 'user-a'
USER_FRIENDSHIP = 'user-f'
SYS_ALL = 'sys-a'

APP_FEED_TYPE = (
    (FILM_RATE, u"Оценка фильма"),
    (FILM_SUBSCRIBE, u"Подписка на фильм"),
    (FILM_NOTWATCH, u"Установлен признак 'не смотреть'"),
    (FILM_COMMENT, u"Комментарий к фильму"),
    (FILM_O, u"Фильм появился в кинотеатре"),
    (PERSON_SUBSCRIBE, u"Подписка на персону"),
    (PERSON_O, u"Появление фильма с участием персоны"),
    (USER_ASK, u"Предложение дружить"),
    (USER_FRIENDSHIP, u"Юзеры друзья"),
    (SYS_ALL, u"Системное сообщение"),
)

APP_NOTIFICATION_TEMPLATE = {
    FILM_O: "notifcation_film.html",
    PERSON_O: "notification_person.html",
}

APP_NOTIFICATION_EMAIL_SUBJECT = {
    FILM_O: APP_SUBJECT_TO_NOTIFICATION_FILM,
    PERSON_O: APP_SUBJECT_TO_NOTIFICATION_PERSON,
}
