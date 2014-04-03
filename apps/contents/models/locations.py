# coding: utf-8

from django.db import models

from utils.fields.currency_field import CurrencyField
from apps.contents.constants import APP_CONTENTS_LOC_TYPE, APP_CONTENTS_PRICE_TYPE


#############################################################################################################
# Модель Месторасположения контента
class Locations(models.Model):
    content    = models.ForeignKey('Contents', verbose_name=u'Контент')
    type       = models.SmallIntegerField(choices=APP_CONTENTS_LOC_TYPE, verbose_name=u'Тип')
    lang       = models.CharField(max_length=40, verbose_name=u'Язык')
    quality    = models.CharField(max_length=40, verbose_name=u'Качество')
    subtitles  = models.CharField(max_length=40, verbose_name=u'Субтитры')
    price      = CurrencyField(verbose_name=u'Цена')
    price_type = models.SmallIntegerField(choices=APP_CONTENTS_PRICE_TYPE, verbose_name=u'Тип цены')
    value      = models.CharField(max_length=40, verbose_name=u'Ценность')


    def __unicode__(self):
        return u'[{:s}] {:s} {:s}'.format(self.pk, self.content.name, self.type)

    class Meta:
        # Имя таблицы в БД
        db_table = 'locations'
        app_label = 'contents'
        verbose_name = u'Месторасположения контента'
        verbose_name_plural = u'Месторасположения контента'
