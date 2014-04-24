# coding: utf-8
from django.db import models


class Cities(models.Model):

    country_id = models.ForeignKey('Countries', verbose_name=u'Название страны', related_name='cities')
    name       = models.CharField(max_length=255, verbose_name=u'Название города')
    name_orig  = models.CharField(max_length=255, verbose_name=u'Оригинальное название города')

    def  __unicode__(self):
        return u'[{0}] {1}'.format(self.pk, self.name)

    class Meta:
        db_table = 'cities'
        app_label = 'films'
        verbose_name = u'Город'
        verbose_name_plural = u'Города'