# coding: utf-8

from django.db import models
from apps.casts.constants import APP_CASTS_PRICE_TYPE


################################################################################
# Модель Пользовательских трансляций
class CastsLocations(models.Model):
    cast_service = models.ForeignKey('CastsServices', verbose_name=u'Сервис трансляций')
    cast       = models.ForeignKey('Casts', verbose_name=u'Трансляция', related_name='cl_location_rel')
    quality    = models.CharField(max_length=255, default='', blank=True, db_index=True, verbose_name=u'Качество')
    price_type = models.IntegerField(null=True, blank=True, choices=APP_CASTS_PRICE_TYPE , db_index=True, verbose_name=u'Тип цены')
    price      = models.FloatField(null=True, blank=True, verbose_name=u'Цена')
    offline    = models.BooleanField(default=True, verbose_name=u"Оффлайн ?")
    url_view   = models.CharField(max_length=255, default='', blank=True, db_index=True, verbose_name=u'Ссылка')
    value      = models.CharField(max_length=255, default='', blank=True, db_index=True, verbose_name=u'Значение')


    def __unicode__(self):
        return u'[{0}] {1} - {2}'.format(self.pk, self.cast_service, self.cast) 

    class  Meta:
        # Имя таблицы в БД
        db_table = 'casts_locations'
        app_label = 'casts'
        verbose_name = u'Ссылка на трансляцию'
        verbose_name_plural = u'Ссылки на трансляции'
