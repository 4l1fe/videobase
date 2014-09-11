# coding: utf-8

import datetime

from django.db import models
from ..constants import *

from djorm_pgfulltext.models import SearchManager
from djorm_pgfulltext.fields import VectorField


#############################################################################################################
#
class FilmManager(models.Manager):
    def get_query_set(self):
        return super(FilmManager, self).get_query_set().filter(type=APP_FILM_FULL_FILM)


#############################################################################################################
# Модель фильмов/сериалов
class Films(models.Model):
    name             = models.CharField(max_length=255, db_index=True, blank=False, verbose_name=u'Название фильма')
    type             = models.CharField(max_length=255, db_index=True, choices=APP_FILM_FILM_TYPES, verbose_name=u'Тип фильма')
    world_release_date = models.DateField(null=True, blank=True, db_index=True, verbose_name=u'Мировая дата выхода')
    release_date     = models.DateField(null=True, blank=True, db_index=True, verbose_name=u'Дата выхода')
    duration         = models.IntegerField(null=True, blank=True, verbose_name=u'Продолжительность фильма')
    budget           = models.IntegerField(null=True, blank=True, verbose_name=u'Бюджет фильма')
    description      = models.TextField(default='', blank=True, verbose_name=u'Описание фильма')
    rating_local     = models.FloatField(null=True, blank=True, db_index=True, default=0, verbose_name=u'Рейтинг фильма по мнению пользователей нашего сайта')
    rating_local_cnt = models.IntegerField(null=True, blank=True, db_index=True, default=0, verbose_name=u'Количество пользователей нашего сайта оценивших фильм')
    imdb_id          = models.IntegerField(null=True, blank=True, verbose_name=u'Порядковый номер на IMDB')
    rating_imdb      = models.FloatField(null=True, blank=True, default=0, verbose_name=u'Рейтинг фильма на сайте imdb.com')
    rating_imdb_cnt  = models.IntegerField(null=True, blank=True, default=0, verbose_name=u'Количество пользователей imdb.com оценивших этот фильм')
    rating_cons      = models.FloatField(null=True, blank=True, default=0, verbose_name=u'Консолидированный рейтинг')
    rating_cons_cnt  = models.IntegerField(null=True, blank=True, db_index=True, default=0, verbose_name=u'Количество голосов консолидированного рейтинга')
    rating_sort      = models.IntegerField(null=True, blank=True, db_index=True, default=0, verbose_name=u'Условный рейтинг для сортировки')
    kinopoisk_id     = models.IntegerField(unique=True, db_index=True, verbose_name=u'Порядковый номер на кинопоиске')
    age_limit        = models.PositiveSmallIntegerField(null=True, blank=True, db_index=True, verbose_name=u'Ограничение по возрасту')
    kinopoisk_lastupdate = models.DateTimeField(null=True, blank=True, verbose_name=u'Дата последнего обновления на кинопоиске')
    rating_kinopoisk     = models.FloatField(null=True, blank=True, verbose_name=u'Рейтинг фильма на сайте kinopoisk.ru')
    rating_kinopoisk_cnt = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=u'Количество пользователей kinopoisk.ru оценивших этот фильм')
    seasons_cnt = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=u'Количество сезонов')
    name_orig   = models.CharField(max_length=255, default='', blank=True, db_index=True, verbose_name=u'Оригинальное название фильма')
    countries   = models.ManyToManyField('Countries', verbose_name=u'Страны производители', related_name='countries')
    genres      = models.ManyToManyField('Genres', verbose_name=u'Жанры', related_name='genres')
    persons     = models.ManyToManyField('Persons', through='PersonsFilms', verbose_name=u'Персоны', related_name='persons')
    was_shown     = models.BooleanField(default=False, verbose_name=u'Фильм отображался в новинках')
    search_index = VectorField()


    get_film_type = FilmManager()
    objects = models.Manager()
    search_manager = SearchManager(
        fields=('name', 'name_orig'),
        config='pg_catalog.english',
        search_field='search_index',
        auto_update_search_field=True
    )


    def __unicode__(self):
        if type(self.name) is str:
            name = unicode(self.name)
        else:
            name = self.name
        return u'[{0}] {1}'.format(self.pk, name)


    @classmethod
    def similar_api(cls, film):
        """
            Выборка похожих фильмов
        """

        params = [','.join([str(i.pk) for i in film.genres.all()]), film.id, APP_FILMS_API_DEFAULT_PER_PAGE]

        # Выполняем запрос, если у фильма есть жанры
        if params[0]:
            sql = """
            SELECT "films".* FROM (
              SELECT DISTINCT ON ("films"."id") films.id AS d, "films".*
              FROM "films" INNER JOIN "films_genres" ON ("films"."id" = "films_genres"."films_id")
              WHERE "films_genres"."genres_id" IN ({0})
            ) as films
            WHERE "films"."id" != {1}
            ORDER BY "films"."rating_sort" DESC LIMIT {2};
            """.format(*params)

            return cls.objects.raw(sql)

        return []


    @classmethod
    def similar_default(cls, limit=True):
        o_similar = cls.objects.order_by('-rating_sort')

        if limit:
            o_similar = o_similar[:APP_FILMS_API_DEFAULT_PER_PAGE]

        return o_similar


    @property
    def get_rating_for_vb_film(self):
        return {
            'imdb': [self.get_rating_imdb, self.rating_imdb_cnt],
            'kp': [self.get_rating_kinopoisk, self.rating_kinopoisk_cnt],
            'cons': [self.get_rating_cons, self.rating_cons_cnt],
            'vsevi': [self.get_rating_local, self.rating_local_cnt],
        }


    @property
    def get_rating_local(self):
        rating = self.rating_local
        if not rating is None:
            return int(rating) if rating.is_integer() else round(rating, 1)

        return rating


    @property
    def get_rating_imdb(self):
        rating = self.rating_imdb
        if not rating is None:
            return int(rating) if rating.is_integer() else round(rating, 1)

        return rating


    @property
    def get_rating_kinopoisk(self):
        rating = self.rating_kinopoisk
        if not rating is None:
            return int(rating) if rating.is_integer() else round(rating, 1)

        return rating


    @property
    def get_rating_cons(self):
        rating = self.rating_cons
        if not rating is None:
            return int(rating) if rating.is_integer() else round(rating, 1)

        return rating


    @property
    def get_rating_local_cnt(self):
        rating_local_cnt = self.rating_local_cnt
        return rating_local_cnt if not rating_local_cnt is None else 0


    @property
    def get_rating_imdb_cnt(self):
        rating_imdb_cnt = self.rating_imdb_cnt
        return rating_imdb_cnt if not rating_imdb_cnt is None else 0


    @property
    def get_rating_kinopoisk_cnt(self):
        rating_kinopoisk_cnt = self.rating_kinopoisk_cnt
        return rating_kinopoisk_cnt if not rating_kinopoisk_cnt is None else 0


    @property
    def get_calc_rating_cons_cnt(self):
        """
            Высчитывается как сумма значений rating_local_cnt, rating_imdb_cnt, rating_kinopoisk_imdb
        """

        return self.get_rating_local_cnt + self.get_rating_imdb_cnt + self.get_rating_kinopoisk_cnt


    @property
    def get_time_factor(self):
        """
            - если release_date - текущая дата >= 700 дней, то time_factor = 1
            - если release_date - текущая дата < 700 дней, но больше 1, то time_factor = 1.5 - 0.5 * (release_date - текущая дата дней) / 700
            - если release_date - текущая дата <= 1, то time_factor = 1.5
        """

        days = 0
        if not self.release_date is None:
            days = (datetime.date.today() - self.release_date).days

        if days >= 700:
            time_factor = 1
        elif 1 < days < 700:
            time_factor = 1.5 - 0.5 * (-days) / 700
        else:
            time_factor = 1.5

        return time_factor


    @property
    def get_calc_rating_cons(self):
        """
            Высчисление rating_cons по следующей формуле: 60% rating_kinopoisk + 30% rating_imdb + 10% rating_local.
            причём, если какое-то значение отсутствует или нулевое,
            то его доля распределяется между остальными значениями, например:
                - если rating_imdb не установлен, то формула становится 85.7% rating_kinpoisk + 14.3% rating_local
                - если rating_kinopoisk не установлен, то формула становится 75% rating_imdb + 25% rating_local
                - если rating_local не установлен, то формула становится 66.7% rating_kinopoisk + 33.3% rating_imdb
                - если rating_imdb и rating_kinopoisk не установлены, то формула становится 100% rating_local
        """

        values = ((6, self.rating_kinopoisk), (3, self.rating_imdb), (1, self.rating_local),)
        divisor = float(sum(t[0] for t in values if t[1]))
        result = sum([t[0] / divisor * t[1] for t in values if t[1]])

        return round(result, 1)


    def get_sort_cnt(self, rating_cons_cnt):
        """
            - если rating_cons_cnt больше 30 000, то sort_cnt = 5 000 + (sort_cnt - 30 000) / 150 + 15 000 / 50 + 10 000 / 20
            - если rating_cons_cnt больше 15 000, но меньше 30 000, sort_cnt = 5 000 + (rating_cons_cnt - 15000) / 50 + 10 000 / 20
            - если rating_cons_cnt больше 5 000, но меньше 15 000, то sort_cnt = 5 000 + (rating_cons_cnt - 5000) / 20
            - если rating_cons меньше или равно 5 000, то sort_cnt = rating_cons_cnt
        """

        if rating_cons_cnt > 30000:
            sort_cnt = 5000 + (rating_cons_cnt - 30000) / 150 + 15000 / 50 + 10000 / 20
        elif 15000 < rating_cons_cnt <= 30000:
            sort_cnt = 5000 + (rating_cons_cnt - 15000) / 50 + 10000 / 20
        elif 5000 < rating_cons_cnt <= 15000:
            sort_cnt = 5000 + (rating_cons_cnt - 5000) / 20
        else:
            sort_cnt = rating_cons_cnt

        return sort_cnt


    @classmethod
    def get_newest_films(cls, limit=4):
        """
            Выбираем четыре последних новинки из фильмов
        """

        sql = """
        SELECT "films".*
        FROM (SELECT DISTINCT ON ("locations"."content_id") "locations"."content_id", "locations"."id" FROM "locations") AS loc
            INNER JOIN "content" ON ("loc"."content_id" = "content"."id")
            INNER JOIN "films" ON ("content"."film_id" = "films"."id")
        WHERE ("films"."rating_cons" >= %s AND "films"."rating_cons_cnt" > %s AND "films"."was_shown" = False)
        ORDER BY "loc"."id" DESC LIMIT %s;
        """

        return cls.objects.raw(sql, params=[6, 5000, limit])


    class Meta(object):
        # Имя таблицы в БД
        db_table = 'films'
        app_label = 'films'
        verbose_name = u'Фильм'
        verbose_name_plural = u'Фильмы'
