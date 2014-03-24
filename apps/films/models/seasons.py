# coding: utf-8

from django.db import models


#############################################################################################################
# Модель Сезонов фильмов/сериалов
class Seasons(models.Model):
    film         = models.ForeignKey('Films', verbose_name=u'Фильм')
    release_date = models.DateTimeField(verbose_name=u'Дата выхода сезона')
    series_cnt   = models.PositiveSmallIntegerField(verbose_name=u'Количество серий в сезоне')
    description  = models.TextField(verbose_name=u'Описание сезона')
    number       = models.PositiveSmallIntegerField(verbose_name=u'Порядковый номер сезона')


    def __unicode__(self):
        return u'[{0}] {1} {2}'.format(self.pk, self.film.name, self.number)

    class  Meta(object):
        # Имя таблицы в БД
        db_table = 'seasons'
        app_label = 'films'
        verbose_name = u'Сезон'
        verbose_name_plural = u'Сезоны'
        unique_together = (('film', 'number'),)
