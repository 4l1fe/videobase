# coding: utf-8
from django.db import models
from django.contrib.auth.models import User
from ..constants import APP_USER_PIC_DIR, APP_USER_PIC_TYPES, APP_USER_PIC_TYPE_LOCAL
from utils.common import get_image_path
import os


################################################################################
# Модель пользовательских картинок
class UsersPics(models.Model):
    user  = models.ForeignKey(User, verbose_name=u'Пользователь', related_name='pics')
    type  = models.CharField(max_length=255, verbose_name=u'Тип', choices=APP_USER_PIC_TYPES, default=APP_USER_PIC_TYPE_LOCAL)
    image = models.ImageField(upload_to=get_image_path, verbose_name=u'Аватарка')

    @property
    def get_upload_to(self):
        return APP_USER_PIC_DIR

    @property
    def filename(self):
        return os.path.basename(self.image.file.name)

    @classmethod
    def get_picture(cls, profile):
        path = u''
        try:
            image = cls.objects.get(id=profile.userpic_id).image
            path = image.storage.url(image.name)
        except Exception, e:
            pass

        return path

    def __unicode__(self):
        return u'[%s] %s : %s' % (self.pk, self.user, self.filename, )

    class Meta:
        # Имя таблицы в БД
        db_table = 'users_pics'
        app_label = 'users'
        verbose_name = u'Картинки пользователя'
        verbose_name_plural = u'Картинки пользователей'
