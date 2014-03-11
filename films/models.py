# coding: utf-8
from django.db import models
from apps.users.models import Users

class Countries(models.Model):
    name = models.CharField(max_length = 255, verbose_name = u'Русское название страны')
    name_orig = models.CharField(max_length =255, verbose_name = u'Название страны на ее языке')
    description = models.TextField()

    def __unicode__(self):
        return u' [%s] %s' % (self.pk, self.name)
    class  Meta(object):
        verbose_name = u"Страна"
        verbose_name_plural = u"Страны"

    
class Genres(models.Model):

    name = models.CharField(max_length =255, verbose_name =u"Название жанра")
    description  = models.TextField(verbose_name = u"Описание жанра")

    class  Meta(object):
        verbose_name = u"Жанр"
        verbose_name_plural = u"Жанры"
    def __unicode__(self):
        return u' [%s] %s' % (self.pk, self.name)

class Films(models.Model):
    name = models.CharField(max_length = 255, verbose_name = u'Название фильма')
    ftype = models.CharField(max_length = 255, verbose_name = u'Жанр')
    fReleaseDate = models.DateTimeField(verbose_name =u'Дата выхода')
    fMonth = models.PositiveSmallIntegerField(verbose_name = u'Месяц (возможно стоит изменить описание)')
    description = models.TextField(verbose_name = u'Описание фильма')
    rating_local = models.PositiveSmallIntegerField(verbose_name = u'Рейтинг фильма по мнению пользователей нашего сайта')
    rating_local_cnt = models.PositiveSmallIntegerField(verbose_name = u'Количество пользователей нашего сайта оценивших фильм')
    rating_imdb = models.PositiveSmallIntegerField(verbose_name = u'Рейтинг фильма на сайте imdb.com')
    rating_imdb_cnt = models.IntegerField(verbose_name = u'Количество пользователей imdb.com оценивших этот фильм')
    rating_kinopoisk = models.PositiveSmallIntegerField(verbose_name = u'Рейтинг фильма на сайте kinopoisk.ru')
    rating_kinopoisk_cnt = models.PositiveSmallIntegerField(verbose_name = u'Количество пользователей kinopoisk.ru оценивших этот фильм')
    seasons_cnt=models.PositiveSmallIntegerField(verbose_name = u'Количество сезонов')
    name_orig = models.CharField(max_length = 255,verbose_name = u'Оригинальное название фильма')
    poster_id = models.IntegerField(verbose_name = u'Идентификатор постера')

    countries = models.ManyToManyField(Countries, verbose_name = u'Страны производители', related_name ='countries')
    genres = models.ManyToManyField(Countries, verbose_name = u'Жанры', related_name = "genres")


    
    def __unicode__(self):
        return u' [%s] %s' % (self.pk, self.name)


    class  Meta(object):
        verbose_name = u"Фильм"
        verbose_name_plural = u"Фильмы"
        

class UsersFilms(models.Model):
    users_id = models.ForeignKey(Users,verbose_name =u'Идентификатор пользоваля')
    films_id = models.ForeignKey(Films)
    ufStatus = models.IntegerField(verbose_name = u'Статус фильма с т.з. пользователя')
    ufRating = models.IntegerField(verbose_name = u'Рейтинг фильма поставленный пользователем')
    subscribed = models.IntegerField(verbose_name = u'Статус подписки')

    def __unicode__(self):
        return u'[%s] %s %s' % (self.pk, self.users_id,self.films_id, self.ufStatus,self.ufRating, self.lastname)

    class  Meta(object):
        verbose_name = u"Связь Фильм-Пользователь"

        
        
class FilmExtras(models.Model):

    Film_id = models.ForeignKey(Films)
    eType = models.CharField(max_length = 255, verbose_name = u"Тип дополнительного материала")
    name = models.CharField(max_length = 255, verbose_name = u'Название')
    name_orig = models.CharField(max_length = 255, verbose_name = u'Оригинальное название')
    description = models.TextField()
    url = models.URLField(max_length = 255, verbose_name = u'Оригинальное название')
    class  Meta(object):
        verbose_name = u"Дополнительный материал"
        verbose_name_plural = u"Дополнительные материалы"

    def __unicode__(self):
        return u' [%s] %s' % (self.pk, self.name)

    
class Seasons(models.Model):
    
    Film_id = models.ForeignKey(Films)
    sReleaseDate = models.DateTimeField(verbose_name = u'Дата выхода сезона')
    series_cnt = models.PositiveSmallIntegerField(verbose_name = u'Количество серий в сезоне')
    description = models.TextField(verbose_name = u'Описание сезона')
    sNumber = models.PositiveSmallIntegerField(verbose_name =u'Порядковый номер сезона')

    class  Meta(object):
        verbose_name = u"Сезон"
        verbose_name_plural = u"Сезоны"


    def __unicode__(self):
        return u' [%s] %s %s' % (self.pk, self.Film_id, self.sNumber)
    

