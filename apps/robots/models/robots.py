# coding: utf-8

from django.db import models
import json


#############################################################################################################
# Модель Роботов
class Robots(models.Model):
    name        = models.CharField(max_length=255, primary_key=True, verbose_name=u'Имя')
    description = models.TextField(verbose_name=u'Описание робота')
    last_start  = models.DateTimeField(verbose_name=u'Дата последнего старта')
    delay       = models.IntegerField(verbose_name=u'Время между стартами в минутах')
    state       = models.TextField(verbose_name=u'Состояние между запусками')

    def __unicode__(self):
        return u' "id": "{0}" name = {1} last_start = {2}'.format(self.pk, self.name, self.last_start)

    class Meta:
        # Имя таблицы в БД
        db_table = 'robots'
        app_label = 'robots'
        verbose_name = u'Робот'
        verbose_name_plural = u'Роботы'
