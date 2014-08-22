# coding: utf-8

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

from apps.films.constants import APP_USERFILM_STATUS, APP_USERFILM_STATUS_UNDEF, \
                                 APP_USERFILM_SUBS_FALSE, APP_USERFILM_SUBS, APP_USERFILM_SUBS_TRUE

from apps.casts.models import CastsServices, Casts

#############################################################################################################
# Модель Пользовательских трансляций
class CastsLocations(models.Model):
    cast       = models.ForeignKey(Casts, verbose_name=u'Идентификатор пользоваля', related_name='uf_users_rel')
    cast_service = models.ForeignKey(CastsServices, verbose_name=u'Идентификатор пользоваля', related_name='uf_users_rel')
    
    quality   = models.CharField(max_length=255, default='', blank=True, db_index=True, verbose_name=u'Оригинальное название фильма')
    price_type =  models.IntegerField(null=True, blank=True, verbose_name=u'Бюджет фильма')
    price =  models.FloatField(null=True, blank=True, verbose_name=u'Бюджет фильма')
    offline = models.BooleanField(default = True, verbose_name = "Is offline now")
    url_view   = models.CharField(max_length=255, default='', blank=True, db_index=True, verbose_name=u'Оригинальное название фильма')
    value   = models.CharField(max_length=255, default='', blank=True, db_index=True, verbose_name=u'Оригинальное название фильма')
    rating     = models.PositiveSmallIntegerField(null=True, blank=True, db_index=True, verbose_name=u'Рейтинг поставленный пользователем')

    def __unicode__(self):
        return u'[{0}] {1} - {2}
        '.format(self.pk, self.user.username, self.cast.name)

        
    class  Meta(object):
        # Имя таблицы в БД
        db_table = 'casts_locations'
        app_label = 'casts'
        verbose_name = u'Трансляции пользователя'
        verbose_name_plural = u'Трансляции пользователей'
        
    
    
