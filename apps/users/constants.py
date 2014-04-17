# coding: utf-8

import os
from videobase.settings import STATIC_PATH

#############################################################################################################
APP_USER_PIC_DIR = os.path.join(STATIC_PATH, 'upload', 'users', 'user_pic')

#############################################################################################################
APP_USER_REL_TYPE_FRIENDS = 'FRIENDS'
APP_USER_REL_TYPE_NONE = 'NONE'
APP_USER_REL_TYPE_COLLEAGUES = 'COLLEAGUES'

APP_USER_REL_TYPES = (
    (APP_USER_REL_TYPE_NONE, 'None'),
    (APP_USER_REL_TYPE_FRIENDS, 'Friends'),
    (APP_USER_REL_TYPE_COLLEAGUES, 'Colleagues'),
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

SUBJECT_TO_RESTORE_PASSWORD = u'Востановление пароля'
