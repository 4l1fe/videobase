# coding: utf-8

from django.db import models


#############################################################################################################
# Модель жанров фильмов/сериалов
class Genres(models.Model):
    name        = models.CharField(max_length=255, verbose_name=u'Название жанра')
    description = models.TextField(verbose_name=u'Описание жанра')

    def __unicode__(self):
        return u'[{0}] {1}'.format(self.pk, self.name)

    def get_cache_key(self):
        return u'{0}-{1}-{2}'.format(self._meta.app_label, self._meta.db_table, 'all')

    class Meta(object):
        # Имя таблицы в БД
        db_table = 'genres'
        app_label = 'films'
        verbose_name = u'Жанр'
        verbose_name_plural = u'Жанры'
