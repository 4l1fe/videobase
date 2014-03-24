# coding: utf-8

from django.db import models


#############################################################################################################
# Модель Пользовательской социальности
class UsersSocials(models.Model):
    user    = models.ForeignKey('Users', verbose_name=u'Пользователь')
    stype   = models.CharField(max_length=255, verbose_name=u'')
    stoken  = models.CharField(max_length=255, verbose_name=u'')
    suserid = models.IntegerField(verbose_name=u'')
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=u'Дата создания')
    sphoto  = models.IntegerField(verbose_name=u'')


    def __unicode__(self):
        return u'[%s] %s - %s' % (self.pk, self.user.name, self.stoken)

    class Meta:
        # Имя таблицы в БД
        db_table = 'users_socials'
        app_label = 'users'
        verbose_name = u'Социальность пользователя'
        verbose_name_plural = u'Социальность пользователей'
