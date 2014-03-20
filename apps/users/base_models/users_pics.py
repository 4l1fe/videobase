# coding: utf-8

from django.db import models


#############################################################################################################
# Модель пользовательских картинок
class UsersPics(models.Model):
    user = models.ForeignKey('Users', verbose_name=u'Пользователь')
    url  = models.CharField(max_length=255, verbose_name=u'Url')


    def __unicode__(self):
        return u'[%s] %s : %s' % (self.pk, self.user.name, self.url)

    class Meta:
        # Имя таблицы в БД
        db_table = 'users_pics'
        app_label = 'Users'
        verbose_name = u'Картинки пользователя'
        verbose_name_plural = u'Картинки пользователей'
