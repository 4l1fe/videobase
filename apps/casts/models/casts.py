# coding: utf-8

from django.db import models
from djorm_pgfulltext.models import SearchManager
from djorm_pgfulltext.fields import VectorField


#############################################################################################################
# Модель Пользовательских фильмов
class Casts(models.Model):
    title       = models.CharField(max_length=255, db_index=True, blank=False, verbose_name=u'Название трансляции')
    title_orig  = models.CharField(max_length=255, db_index=True, blank=False, verbose_name=u'Название оригинала')
    start       = models.DateTimeField(auto_now_add=True, verbose_name=u'Время начала трансляции')
    duration    = models.IntegerField(null=True, blank=True, verbose_name=u'Продолжительность')
    status      = models.CharField(max_length=255, db_index=True, blank=False, verbose_name=u'Статус')
    description = models.TextField(max_length=255, db_index=True, blank=False, verbose_name=u'Описание')
    pg_rating   = models.CharField(max_length=255, db_index=True, blank=False, verbose_name=u'Возрастной рейтинг')
    tags        = models.ManyToManyField('AbstractCastsTags', verbose_name=u'Tags', related_name='casts')
    search_index = VectorField()

    objects = models.Manager()
    search_manager = SearchManager(
        fields=('title', 'title_orig'),
        config='pg_catalog.english',
        search_field='search_index',
        auto_update_search_field=True
    )

    def __unicode__(self):
        return u'[{0}] {1}'.format(self.pk, self.title)

    class Meta:
        # Имя таблицы в БД
        db_table = 'casts'
        app_label = 'casts'
        verbose_name = u'Трансляция'
        verbose_name_plural = u'Трансляции'
