# coding: utf-8

import os
from videobase.settings  import STATIC_PATH

# Путь к каталогу с фото

PERSON_PHOTO_DIR =  os.path.join(STATIC_PATH, 'upload', 'people', 'photos')
USER_PIC_DIR =  os.path.join(STATIC_PATH, 'upload', 'users', 'user_pic')

REL_TYPES = (
    ('FRIENDS', 'Friends'),
    ('COLLEAGUES', 'Colleagues'),
)


USER_ACTIVE  = 0
USER_INACTIVE = 1

USER_STATUS = (
    (USER_ACTIVE,  u'Активный'),
    (USER_INACTIVE, u'Заблокирован')
)

USER_PIC_TYPES = (
    ('SOCIAL', 'Из социальных сетей'),
    ('LOCAL', 'Сохранные изображения')
)
