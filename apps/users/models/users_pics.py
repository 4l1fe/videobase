# coding: utf-8

from django.db import models
from django.contrib.auth.models import User

from ..constants import APP_USER_PIC_DIR
from utils.common import get_image_path


#############################################################################################################
# Модель пользовательских картинок
class UsersPics(models.Model):
    user = models.ForeignKey(User, verbose_name=u'Пользователь')
    url  = models.ImageField(upload_to=get_image_path, verbose_name=u'Аватарка')

    def __unicode__(self):
        return u'[%s] %s : %s %s' % (self.pk, self.user, self.url, self.url.url)

    class Meta:
        # Имя таблицы в БД
        db_table = 'users_pics'
        app_label = 'users'
        verbose_name = u'Картинки пользователя'
        verbose_name_plural = u'Картинки пользователей'
