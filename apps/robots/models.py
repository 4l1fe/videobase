# coding: utf-8

from django.db import models


#############################################################################################################
# Роботы
class Robots(models.Model):
    name        = models.CharField(max_length=255, primary_key=True, verbose_name=u'Имя')
    description = models.TextField(verbose_name=u'Описание робота')
    last_start  = models.DateTimeField(verbose_name=u'Дата последнего старта')
    next_start  = models.DateTimeField(verbose_name=u'Дата следующего старта')
    rstatus     = models.IntegerField(verbose_name=u'Статус')


    def __unicode__(self):
        return u'[%s] %s' % (self.pk, self.name,)

    class Meta:
        # Имя таблицы в БД
        db_table = 'robots'
        verbose_name = u'Робот'
        verbose_name_plural = u'Роботы'


#############################################################################################################
# Логирование роботов
class RobotsLog(models.Model):
    robot_name = models.ForeignKey(Robots, verbose_name=u'Имя робота')
    created    = models.DateTimeField(verbose_name=u'Дата следующего старта')
    value      = models.CharField(max_length=255, verbose_name=u'Значение')
    itype      = models.IntegerField(choices=(), verbose_name=u'Тип')


    def __unicode__(self):
        return u'[%s] %s' % (self.pk, self.name,)

    class Meta:
        # Имя таблицы в БД
        db_table = 'robots_log'
        verbose_name = u'Логирование робота'
        verbose_name_plural = u'Логирование роботов'
