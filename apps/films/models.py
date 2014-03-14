# coding: utf-8

from django.db import models

from constants import *
from apps.users.models import Users,Persons


#############################################################################################################
# Таблица Стран
class Countries(models.Model):
    name        = models.CharField(max_length=255, verbose_name=u'Русское название страны')
    name_orig   = models.CharField(max_length=255, verbose_name=u'Название страны на ее языке')
    description = models.TextField(verbose_name=u'Описание')

    def __unicode__(self):
        return u' [%s] %s' % (self.pk, self.name)


    class  Meta(object):
        # Имя таблицы в БД
        db_table = 'countries'
        verbose_name = u'Страна'
        verbose_name_plural = u'Страны'


#############################################################################################################
# Таблица жанров фильмов/сериалов
class Genres(models.Model):
    name         = models.CharField(max_length=255, verbose_name=u'Название жанра')
    description  = models.TextField(verbose_name=u'Описание жанра')

    def __unicode__(self):
        return u' [%s] %s' % (self.pk, self.name)

    class  Meta(object):
        # Имя таблицы в БД
        db_table = 'genres'
        verbose_name = u'Жанр'
        verbose_name_plural = u'Жанры'


#############################################################################################################
# Таблица фильмов/сериалов
class Films(models.Model):
    name             = models.CharField(max_length=255, verbose_name=u'Название фильма')
    ftype            = models.CharField(max_length=255, choices=APP_FILM_FILM_TYPES, verbose_name=u'Тип фильма')
    frelease_date    = models.DateField(verbose_name=u'Дата выхода')
    fduration        = models.IntegerField(null=True, blank=True, verbose_name=u'Продолжительность фильма')
    fbudget          = models.IntegerField(null=True, blank=True, verbose_name=u'Бюджет фильма')
    description      = models.TextField(default='', blank=True, verbose_name=u'Описание фильма')
    rating_local     = models.FloatField(null=True, blank=True, verbose_name=u'Рейтинг фильма по мнению пользователей нашего сайта')
    rating_local_cnt = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=u'Количество пользователей нашего сайта оценивших фильм')
    rating_imdb      = models.FloatField(null=True, blank=True, verbose_name=u'Рейтинг фильма на сайте imdb.com')
    rating_imdb_cnt  = models.IntegerField(null=True, blank=True, verbose_name=u'Количество пользователей imdb.com оценивших этот фильм')
    kinopoisk_id     = models.IntegerField(null=True, blank=True, verbose_name=u'Порядковый номер на кинопоиске')
    age_limit        = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=u'Ограничение по возрасту')
    kinopoisk_lastupdate = models.DateTimeField(null=True, blank=True, verbose_name=u'Дата последнего обновления на кинопоиске')
    rating_kinopoisk     = models.FloatField(null=True, blank=True, verbose_name=u'Рейтинг фильма на сайте kinopoisk.ru')
    rating_kinopoisk_cnt = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=u'Количество пользователей kinopoisk.ru оценивших этот фильм')
    seasons_cnt = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=u'Количество сезонов')
    name_orig   = models.CharField(max_length=255, default='', blank=True, verbose_name=u'Оригинальное название фильма')
    countries   = models.ManyToManyField(Countries, verbose_name=u'Страны производители', related_name='countries')
    genres      = models.ManyToManyField(Genres, verbose_name=u'Жанры', related_name='genres')


    def __unicode__(self):
        return u' [%s] %s' % (self.pk, self.name)

    class  Meta(object):
        # Имя таблицы в БД
        db_table = 'films'
        verbose_name = u'Фильм'
        verbose_name_plural = u'Фильмы'


#############################################################################################################
# Таблица расширения фильмов/сериалов
class FilmExtras(models.Model):
    film        = models.ForeignKey(Films, verbose_name=u'Фильм')
    etype       = models.CharField(max_length=255,
                                   choices=APP_FILM_TYPE_ADDITIONAL_MATERIAL,
                                   verbose_name=u'Тип дополнительного материала')
    name        = models.CharField(max_length=255, verbose_name=u'Название')
    name_orig   = models.CharField(max_length=255, verbose_name=u'Оригинальное название')
    description = models.TextField(verbose_name=u'Описание')
    url         = models.URLField(max_length=255, verbose_name=u'Ссылка на дополнительный материал')


    def __unicode__(self):
        return u' [%s] %s' % (self.pk, self.name)

    class  Meta(object):
        # Имя таблицы в БД
        db_table = 'films_extras'
        verbose_name = u'Дополнительный материал'
        verbose_name_plural = u'Дополнительные материалы'


#############################################################################################################
#
class UsersFilms(models.Model):
    user      = models.ForeignKey(Users, verbose_name=u'Идентификатор пользоваля')
    film      = models.ForeignKey(Films, verbose_name=u'Фильм')
    ufstatus   = models.IntegerField(verbose_name=u'Статус фильма с т.з. пользователя')
    ufrating   = models.IntegerField(verbose_name=u'Рейтинг фильма поставленный пользователем')
    subscribed = models.IntegerField(verbose_name=u'Статус подписки')


    def __unicode__(self):
        return u'[%s] %s - %s (%s)' % (self.pk, self.user.name, self.film.name, self.ufstatus)

    class  Meta(object):
        # Имя таблицы в БД
        db_table = 'users_films'
        verbose_name = u'Связь Фильм-Пользователь'
        verbose_name_plural = u'Связь Фильм-Пользователи'


#############################################################################################################
# Таблица Сезонов фильмов/сериалов
class Seasons(models.Model):
    film         = models.ForeignKey(Films, verbose_name=u'Фильм')
    release_date = models.DateTimeField(verbose_name=u'Дата выхода сезона')
    series_cnt   = models.PositiveSmallIntegerField(verbose_name=u'Количество серий в сезоне')
    description  = models.TextField(verbose_name=u'Описание сезона')
    number       = models.PositiveSmallIntegerField(verbose_name=u'Порядковый номер сезона')


    def __unicode__(self):
        return u' [%s] %s %s' % (self.pk, self.film.name, self.number)

    class  Meta(object):
        # Имя таблицы в БД
        db_table = 'seasons'
        verbose_name = u'Сезон'
        verbose_name_plural = u'Сезоны'
        unique_together = (('film', 'number'),)

        
#############################################################################################################
# Таблица роли персон в производстве фильмов
class PersonsFilms(models.Model):

    film      = models.ForeignKey(Films, verbose_name=u'Фильм')
    person    = models.ForeignKey(Persons, verbose_name=u'Персона')
    p_type    = models.CharField(max_length=255, choices=APP_FILM_PERSON_TYPES, verbose_name=u'Тип персоны')
    p_character = models.CharField(max_length=255, default = '')
    description = models.CharField(max_length=255, default = '')
   
        
    def __unicode__(self):
        return u' [{:s}] {:s} {:s}'.format(self.pk, self.film.name, self.person.name)

        
    class  Meta(object):
        # Имя таблицы в БД
        db_table = 'persons_films'
        verbose_name = u'Роль персоны в производстве фильма'
        verbose_name_plural = u'Роли персон в производстве фильмов'
        unique_together = (('film', 'person'),)

        
