# coding: utf-8
from django.db import models
from djorm_pgfulltext.models import SearchManager
from djorm_pgfulltext.fields import VectorField


################################################################################
# Модель Пользовательских фильмов
class Casts(models.Model):
    title       = models.CharField(max_length=255, db_index=True, blank=False, verbose_name=u'Название трансляции')
    title_orig  = models.CharField(max_length=255, db_index=True, blank=False, verbose_name=u'Название оригинала')
    start       = models.DateTimeField(auto_now_add=True, verbose_name=u'Время начала трансляции')
    duration    = models.IntegerField(null=True, blank=True, verbose_name=u'Продолжительность')
    status      = models.CharField(max_length=255, db_index=True, blank=True, null=True, verbose_name=u'Статус')
    description = models.TextField(max_length=255, blank=True, null=True, verbose_name=u'Описание')
    pg_rating   = models.CharField(max_length=255, blank=True, null=True, verbose_name=u'Возрастной рейтинг')
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

    @classmethod
    def best_old_casts(cls, start_dt=None, end_dt=None, limit=4):
        if not (limit and start_dt and end_dt):
            return []

        sql = """
        SELECT casts.* FROM (
            SELECT casts.id, COUNT(users_casts.cast_id) AS casts_cnt
            FROM casts INNER JOIN users_casts ON casts.id = users_casts.cast_id
            WHERE casts.start > %s AND casts.start < %s AND users_casts.subscribed IS NOT NULL
            GROUP BY users_casts.cast_id, casts.id
            LIMIT %s
        ) AS cs LEFT JOIN casts ON casts.id = cs.id
        ORDER BY cs.casts_cnt DESC
        """

        return cls.objects.raw(sql, params=[start_dt, end_dt, limit])

    @classmethod
    def best_future_casts(cls, start_dt=None, end_dt=None, limit=4):
        if not (limit and start_dt and end_dt):
            return []

        sql = """
        SELECT casts.* FROM (
            SELECT casts.id, COUNT(users_casts.cast_id) AS casts_cnt
            FROM casts INNER JOIN users_casts ON casts.id = users_casts.cast_id
            WHERE casts.start >= %s AND casts.start <= %s AND users_casts.subscribed IS NOT NULL
            GROUP BY users_casts.cast_id, casts.id
            LIMIT %s
        ) AS cs LEFT JOIN casts ON casts.id = cs.id
        ORDER BY cs.casts_cnt DESC
        """

        return cls.objects.raw(sql, params=[start_dt, end_dt, limit])

    class Meta:
        # Имя таблицы в БД
        db_table = 'casts'
        app_label = 'casts'
        verbose_name = u'Трансляция'
        verbose_name_plural = u'Трансляции'
