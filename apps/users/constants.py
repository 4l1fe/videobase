# coding: utf-8

import os


#############################################################################################################
APP_USER_PIC_DIR = os.path.join('upload', 'users', 'user_pic')

#############################################################################################################
APP_USER_REL_TYPE_FRIENDS              = 'f'
APP_USER_REL_TYPE_SEND_NOT_RECEIVED    = 's'
APP_USER_REL_TYPE_ACCEPTED_NOT_ADOPTED = 'r'
APP_USER_REL_TYPE_NONE                 = None

APP_USER_REL_TYPES = (
    (APP_USER_REL_TYPE_FRIENDS, 'Друзья'),
    (APP_USER_REL_TYPE_SEND_NOT_RECEIVED, 'Заявка отправлена, но не принята'),
    (APP_USER_REL_TYPE_ACCEPTED_NOT_ADOPTED, 'Заявка получена, но не принята'),
)

#############################################################################################################
APP_USER_ACTIVE   = 0
APP_USER_INACTIVE = 1

APP_USER_STATUS = (
    (APP_USER_ACTIVE,  u'Активный'),
    (APP_USER_INACTIVE, u'Заблокирован')
)

APP_USER_PIC_TYPE_SOCIAL_VK = 'vk-oauth2'
APP_USER_PIC_TYPE_SOCIAL_FACEBOOK = 'facebook'
APP_USER_PIC_TYPE_SOCIAL_TWITTER = 'twitter'
APP_USER_PIC_TYPE_SOCIAL_GOOGLE = 'google-oauth2'
APP_USER_PIC_TYPE_LOCAL = 'local'

#############################################################################################################
APP_USER_PIC_TYPES = (
    (APP_USER_PIC_TYPE_SOCIAL_VK, 'Vkontakte'),
    (APP_USER_PIC_TYPE_SOCIAL_FACEBOOK, 'Facebook'),
    (APP_USER_PIC_TYPE_SOCIAL_TWITTER, 'Twitter'),
    (APP_USER_PIC_TYPE_SOCIAL_GOOGLE, 'Google+'),
    (APP_USER_PIC_TYPE_LOCAL, 'Из собственных загрузок'),
)

APP_SUBJECT_TO_RESTORE_PASSWORD = u'Востановление пароля'
APP_SUBJECT_TO_RESTORE_EMAIL = u'Смена Email'
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
PERSON_O = 'pers-o'
USER_ASK = 'user-a'
USER_FRIENDSHIP = 'user-f'
SYS_ALL = 'sys-a'

FILM_NEWSLETTER = [FILM_RATE, FILM_SUBSCRIBE, FILM_COMMENT, FILM_O]

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
    FILM_O: "mail/notification_film.html",
    PERSON_O: "mail/notification_person.html",
}

APP_NOTIFICATION_EMAIL_SUBJECT = {
    FILM_O: APP_SUBJECT_TO_NOTIFICATION_FILM,
    PERSON_O: APP_SUBJECT_TO_NOTIFICATION_PERSON,
}


APP_USERPROFILE_PRIVACY_ALL = 0
APP_USERPROFILE_PRIVACY_FRIENDS = 1
APP_USERPROFILE_PRIVACY_MY = 2

APP_USERPROFILE_PRIVACY = (
    (APP_USERPROFILE_PRIVACY_ALL, u'Видно всем'),
    (APP_USERPROFILE_PRIVACY_FRIENDS, u'Видно только друзьям'),
    (APP_USERPROFILE_PRIVACY_MY, u'Видно только мне'),
)

APP_USERPROFILE_NOTIFICATION_DAY = 1
APP_USERPROFILE_NOTIFICATION_WEEK = 7
APP_USERPROFILE_NOTIFICATION_NEVER = 0

APP_USERPROFILE_NOTIFICATION = (
    (APP_USERPROFILE_NOTIFICATION_DAY, u'Один раз в день'),
    (APP_USERPROFILE_NOTIFICATION_WEEK, u'Раз в неделю'),
    (APP_USERPROFILE_NOTIFICATION_NEVER, u'Никогда'),
)

APP_USER_ACTIVE_KEY = 'act_key'

#############################################################################################################
APP_USER_HASH_EMAIL = 1
APP_USER_HASH_PASSWD = 2
APP_USER_HASH_REGISTR = 3

TYPE_PASSWD_HASH = (
    (APP_USER_HASH_EMAIL, u'Смена email'),
    (APP_USER_HASH_PASSWD, u'Смена пароля'),
    (APP_USER_HASH_REGISTR, u'При регистрации'),
)

#############################################################################################################
APP_USER_REQUIRE_AUTH_PAGES = ('stream', 'playlist', 'profile') # страницы требующие авторизации