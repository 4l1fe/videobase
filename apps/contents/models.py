# coding: utf-8

from django.db import models

from utils.fields import CurrencyField
from apps.users.models import Users
from apps.films.models import Films, Seasons


#############################################################################################################
# Таблица контента
class Content(models.Model):
    film                 = models.ForeignKey(Films, verbose_name=u'Фильм')
    name                 = models.CharField(max_length=255, verbose_name=u'Название')
    name_orig            = models.CharField(max_length=255, verbose_name=u'Оригинальное название')
    number               = models.IntegerField(null=True, blank=True, verbose_name=u'Номер сезона')
    description          = models.TextField(verbose_name=u'Описание')
    release_date         = models.DateTimeField(verbose_name=u'Дата выхода')
    season               = models.ForeignKey(Seasons, null=True, blank=True, verbose_name=u'Сезоны')
    viewer_cnt           = models.IntegerField(verbose_name=u'Количество посмотревших за все время')
    viewer_lastweek_cnt  = models.IntegerField(verbose_name=u'Количество посмотревших за последнюю неделю')
    viewer_lastmonth_cnt = models.IntegerField(verbose_name=u'Количество посмотревших за последний месяц')


    def __unicode__(self):
        return u'[{:s}] {:s}'.format(self.pk, self.film.name,)

    class Meta:
        # Имя таблицы в БД
        db_table = 'content'
        verbose_name = u'Место'
        verbose_name_plural = u'Места'


#############################################################################################################
# Таблица месторасположения контента
class Locations(models.Model):
    content    = models.ForeignKey(Content, verbose_name=u'Контент')
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
        verbose_name = u'Место'
        verbose_name_plural = u'Места'


#############################################################################################################
# Таблица комментариев
class Comments(models.Model):
    user       = models.ForeignKey(Users, verbose_name=u'Пользователь')
    content    = models.IntegerField(verbose_name=u'Контент')
    ctext      = models.TextField(verbose_name=u'Tекст комментария')
    parent_id  = models.IntegerField(verbose_name=u'Родительский комментарий')
    cstatus    = models.CharField(max_length=40, verbose_name=u'Статус')
    created    = models.DateTimeField(auto_now_add=True, verbose_name=u'Создан')


    def __unicode__(self):
        return u'[{:s}] {:s} ({:s})'.format(self.pk, self.user.name, self.content)

    class Meta:
        # Имя таблицы в БД
        db_table = 'comments'
        verbose_name = u'Комментарий'
        verbose_name_plural = u'Комментарии'
