# coding: utf-8
from django.db import models


#############################################################################################################
# Модель Логирование роботов
class RobotsLog(models.Model):
    robot_name = models.ForeignKey('Robots', verbose_name=u'Имя робота')
    created    = models.DateTimeField(verbose_name=u'Дата следующего старта')
    value      = models.CharField(max_length=255, verbose_name=u'Значение')
    itype      = models.IntegerField(choices=(), verbose_name=u'Тип')
    try_time   = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=u'Дата попытки')

    def __unicode__(self):
        return u'[{0}] {1}'.format(self.pk, self.name,)

    class Meta:
        # Имя таблицы в БД
        db_table = 'robots_log'
        app_label = 'robots'
        verbose_name = u'Логирование робота'
        verbose_name_plural = u'Логирование роботов'


class RobotsInfoLogging(models.Model):
    robot_name = models.CharField(max_length=255, verbose_name=u'Имя робота')
    locations  = models.CharField(max_length=255, verbose_name=u'Локации')
    log_time   = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=u'Дата лога')

    def __unicode__(self):
        return u'[{0}] {1}'.format(self.pk, self.name,)

    class Meta:
        # Имя таблицы в БД
        db_table = 'robots_logging_info'
        app_label = 'robots'
        verbose_name = u'Логирование информации о работе робота'
        verbose_name_plural = u'Логирование информации о работе роботов'