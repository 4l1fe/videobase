# coding: utf-8

from django.db import models

from utils.fields.currency_field import CurrencyField


#############################################################################################################
# Модель Месторасположения контента
class Locations(models.Model):
    content    = models.ForeignKey('Contents', verbose_name=u'Контент')
    ltype      = models.CharField(max_length=255, choices=[], verbose_name=u'Тип')
    quality    = models.CharField(max_length=40, verbose_name=u'Качество')
    subtitles  = models.CharField(max_length=40, verbose_name=u'Субтитры')
    price      = CurrencyField(verbose_name=u'Цена')
    price_type = models.CharField(max_length=40, verbose_name=u'Тип цены')
    value      = models.CharField(max_length=40, verbose_name=u'Ценность')


    def __unicode__(self):
        return u'[{:s}] {:s} {:s}'.format(self.pk, self.content.name, self.ltype)

    class Meta:
        # Имя таблицы в БД
        db_table = 'locations'
        app_label = 'Contents'
        verbose_name = u'Месторасположения контента'
        verbose_name_plural = u'Месторасположения контента'
