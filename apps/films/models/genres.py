# coding: utf-8

from django.db import models


#############################################################################################################
# Модель жанров фильмов/сериалов
class Genres(models.Model):
    name        = models.CharField(max_length=255, db_index=True, verbose_name=u'Название жанра')
    description = models.TextField(verbose_name=u'Описание жанра')

    def __unicode__(self):
        return u'[{0}] {1}'.format(self.pk, self.name)

    @classmethod
    def get_cache_key(cls):
        return u'{0}-{1}-{2}'.format(cls._meta.app_label, cls._meta.db_table, 'all')

    @classmethod
    def get_all_genres(cls, order=False):
        genres_data = cls.objects.all().values('id', 'name')

        if order:
            genres_data = [
                {'id': genre['id'], 'name': genre['name'], 'order': i}
                for i, genre in enumerate(sorted(genres_data, key=lambda g: g['name']))
            ]

        return genres_data

    class Meta(object):
        # Имя таблицы в БД
        db_table = 'genres'
        app_label = 'films'
        verbose_name = u'Жанр'
        verbose_name_plural = u'Жанры'
