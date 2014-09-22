# coding: utf-8

from django.db import models
from treebeard.ns_tree import NS_Node


#############################################################################################################
# Модель жанров фильмов/сериалов
class Genres(NS_Node):
    name        = models.CharField(max_length=255, db_index=True, verbose_name=u'Название жанра')
    description = models.TextField(verbose_name=u'Описание жанра')
    hidden      = models.NullBooleanField(db_index=True, default=False, verbose_name=u'Скрытый')

    def __unicode__(self):
        return u'[{0}] {1}'.format(self.pk, self.name)

    @classmethod
    def get_cache_key(cls):
        return u'{0}-{1}-{2}'.format(cls._meta.app_label, cls._meta.db_table, 'all')

    @classmethod
    def get_grouped_genres(cls):
        return cls.objects.filter(depth=1, hidden=False).order_by('tree_id', 'name').values('id', 'name')

    @classmethod
    def get_all_genres(cls, get_values=True):
        query = cls.objects.extra(where=['lft-rgt=-1']).order_by('name')
        return query.values('id', 'name') if get_values else query

    @classmethod
    def get_children_list_id(cls, pk):
        try:
            o_genres = cls.objects.get(id=pk)
        except Exception, e:
            return []

        if o_genres.is_root():
            children = o_genres.get_children()
            if len(children):
                list_genres = [i.id for i in o_genres.get_children()]
            else:
                list_genres = [o_genres.id]
        else:
            list_genres = [o_genres.id]

        return list_genres

    class Meta(object):
        # Имя таблицы в БД
        db_table = 'genres'
        app_label = 'films'
        verbose_name = u'Жанр'
        verbose_name_plural = u'Жанры'
