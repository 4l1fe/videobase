# coding: utf-8

from django.db import models


#############################################################################################################
# Модель Роботов
class Robots(models.Model):
    name        = models.CharField(max_length=255, primary_key=True, verbose_name=u'Имя')
    description = models.TextField(verbose_name=u'Описание робота')
    last_start  = models.DateTimeField(verbose_name=u'Дата последнего старта')
    next_start  = models.DateTimeField(verbose_name=u'Дата следующего старта')
    rstatus     = models.IntegerField(verbose_name=u'Статус')
    state       = models.TextField(verbose_name=u'Состояние между запусками')

    def __unicode__(self):
        return u'[{0}] {1}'.format(self.pk, self.name,)

    class Meta:
        # Имя таблицы в БД
        db_table = 'robots'
        app_label = 'robots'
        verbose_name = u'Робот'
        verbose_name_plural = u'Роботы'
