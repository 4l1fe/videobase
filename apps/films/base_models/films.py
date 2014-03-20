# coding: utf-8

from django.db import models
from ..constants import *


#############################################################################################################
# Модель фильмов/сериалов
class Films(models.Model):
    name             = models.CharField(max_length=255, verbose_name=u'Название фильма')
    ftype            = models.CharField(max_length=255, choices=APP_FILM_FILM_TYPES, verbose_name=u'Тип фильма')
    frelease_date    = models.DateField(verbose_name=u'Дата выхода')
    fduration        = models.IntegerField(null=True, blank=True, verbose_name=u'Продолжительность фильма')
    fbudget          = models.IntegerField(null=True, blank=True, verbose_name=u'Бюджет фильма')
    description      = models.TextField(default='', blank=True, verbose_name=u'Описание фильма')
    rating_local     = models.FloatField(null=True, blank=True, verbose_name=u'Рейтинг фильма по мнению пользователей нашего сайта')
    rating_local_cnt = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=u'Количество пользователей нашего сайта оценивших фильм')
    imdb_id          = models.IntegerField(null=True, blank=True, verbose_name=u'Порядковый номер на IMDB')
    rating_imdb      = models.FloatField(null=True, blank=True, verbose_name=u'Рейтинг фильма на сайте imdb.com')
    rating_imdb_cnt  = models.IntegerField(null=True, blank=True, verbose_name=u'Количество пользователей imdb.com оценивших этот фильм')
    kinopoisk_id     = models.IntegerField(null=True, blank=True, verbose_name=u'Порядковый номер на кинопоиске')
    age_limit        = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=u'Ограничение по возрасту')
    kinopoisk_lastupdate = models.DateTimeField(null=True, blank=True, verbose_name=u'Дата последнего обновления на кинопоиске')
    rating_kinopoisk     = models.FloatField(null=True, blank=True, verbose_name=u'Рейтинг фильма на сайте kinopoisk.ru')
    rating_kinopoisk_cnt = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=u'Количество пользователей kinopoisk.ru оценивших этот фильм')
    seasons_cnt = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=u'Количество сезонов')
    name_orig   = models.CharField(max_length=255, default='', blank=True, verbose_name=u'Оригинальное название фильма')
    countries   = models.ManyToManyField('Countries', verbose_name=u'Страны производители', related_name='countries')
    genres      = models.ManyToManyField('Genres', verbose_name=u'Жанры', related_name='genres')


    def __unicode__(self):
        return u'[{0}] {1}'.format(self.pk, self.name)

    class  Meta(object):
        # Имя таблицы в БД
        db_table = 'films'
        app_label = 'Films'
        verbose_name = u'Фильм'
        verbose_name_plural = u'Фильмы'
