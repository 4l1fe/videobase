# coding: utf-8

import os

APP_CASTS_DEFAULT_PAGE = 1
APP_CASTS_CASTS_PER_PAGE = 12

APP_CONTENTS_PRICE_TYPE_FREE = 0
APP_CONTENTS_PRICE_TYPE_PAY = 2


APP_CASTS_PRICE_TYPE = (
    (APP_CONTENTS_PRICE_TYPE_FREE, 'Бесплатно'),
    (APP_CONTENTS_PRICE_TYPE_PAY, 'Платно')
)

APP_CAST_POSTER_DIR = os.path.join('upload', 'castextras')


APP_CASTS_START_NOTIFY = 40
APP_CASTS_MAIL_SUBJECT = u'Уведомление о старте трансляции'
APP_CASTS_MAIL_TEMPLATE = u'cast_notification'

CCU_ONLINE = 'online'
CCU_OFFLINE = 'offline'
CCU_BLOCKED = 'blocked'
CCU_STATUSES = (
    (CCU_ONLINE, u'Онлайн'),
    (CCU_OFFLINE, u'Офлайн'),
    (CCU_BLOCKED, u'Заблокирован')
)
