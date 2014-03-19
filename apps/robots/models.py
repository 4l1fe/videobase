# coding: utf-8

from django.db import models
from constants import APP_ROBOTS_PARSE_TRY_RESULT_TYPES
from apps.films.models import Films
import datetime


#############################################################################################################
# Роботы
class Robots(models.Model):
    name        = models.CharField(max_length=255, primary_key=True, verbose_name=u'Имя')
    description = models.TextField(verbose_name=u'Описание робота')
    last_start  = models.DateTimeField(verbose_name=u'Дата последнего старта')
    next_start  = models.DateTimeField(verbose_name=u'Дата следующего старта')
    rstatus     = models.IntegerField(verbose_name=u'Статус')


    def __unicode__(self):
        return u'[{0}] {1}'.format(self.pk, self.name,)

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
        return u'[{0}] {1}'.format(self.pk, self.name,)

    class Meta:
        # Имя таблицы в БД
        db_table = 'robots_log'
        verbose_name = u'Логирование робота'
        verbose_name_plural = u'Логирование роботов'

class KinopoiskTries(models.Model):

    film = models.ForeignKey(Films,verbose_name = "Фильм")
    try_time = models.DateTimeField(verbose_name=u'Дата попытки')
    result = models.CharField(max_length=255, choices=APP_ROBOTS_PARSE_TRY_RESULT_TYPES, verbose_name=u'Удался ли парсинг')

    def __unicode__(self):
        return u'[{0}] {1}'.format(self.pk, self.film, datetime.datetime.strftime(self.try_time,"%Y-%b-%d %H:%M:%S")
)

    class Meta:
        # Имя таблицы в БД
        db_table = 'robots_kinopoisk_tries'
        verbose_name = u'Попытка взять инфу о фильме с кинопоиска'
        verbose_name_plural = u'Попытки взять инфу о фильме с кинопоиска'
