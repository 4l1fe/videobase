# coding: utf-8

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

from apps.films.constants import APP_USERFILM_STATUS, APP_USERFILM_STATUS_UNDEF, \
                                 APP_USERFILM_SUBS_FALSE, APP_USERFILM_SUBS, APP_USERFILM_SUBS_TRUE


#############################################################################################################
# Модель Пользовательских трансляций
class ExtrasCasts(models.Model):
    cast       = models.ForeignKey('Casts', verbose_name=u'Идентификатор пользоваля')
    extra      = models.IntegerField(null=True, blank=True, verbose_name=u'Бюджет фильма')


    def __unicode__(self):
        return u'[{0}] {1} - {2}'.format(self.pk, self.cast.title, self.extra)

        
    class  Meta(object):
        # Имя таблицы в БД
        db_table = 'extras_casts'
        app_label = 'casts'
        verbose_name = u'Трансляции пользователя'
        verbose_name_plural = u'Трансляции пользователей'
