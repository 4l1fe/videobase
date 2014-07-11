# coding: utf-8

from django.db import models


#############################################################################################################
# Модель Стран
class Countries(models.Model):
    name        = models.CharField(max_length=255, db_index=True, verbose_name=u'Русское название страны')
    name_orig   = models.CharField(max_length=255, verbose_name=u'Название страны на ее языке')
    description = models.TextField(verbose_name=u'Описание')

    def __unicode__(self):
        return u'[{0}] {1}'.format(self.pk, self.name.capitalize())


    class  Meta(object):
        # Имя таблицы в БД
        db_table = 'countries'
        app_label = 'films'
        verbose_name = u'Страна'
        verbose_name_plural = u'Страны'
