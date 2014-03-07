# coding: utf-8

from django.db import models

# Create your models here.
class Users(models.Model):
    firstname = models.CharField(max_length=255, verbose_name=u'')
    lastname  = models.CharField(max_length=255, verbose_name=u'')
    email     = models.EmailField(max_length=255, verbose_name=u'')
    passhash  = models.CharField(max_length=255, verbose_name=u'')
    last_visited = models.DateTimeField(verbose_name=u'')
    created   = models.DateTimeField(verbose_name=u'')
    ustatus   = models.PositiveSmallIntegerField(verbose_name=u'')
    userpic_type = models.CharField(max_length=255, verbose_name=u'')
    userpic_type = models.IntegerField(verbose_name=u'')


    def __unicode__(self):
        return u'[%s] %s %s' % (self.pk, self.firstname, self.lastname)

    class Meta:
        # Имя таблицы в БД
        db_table = 'users'
        verbose_name = u'Пользователь'
        verbose_name_plural = u'Пользователи'



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
    name_org = models.CharField(verbose_name = u'Оригинальное название фильма')
    poster_id = models.IntegerField(verbose_name = u'Идентификатор постера')


    def __unicode__(self):
        return u' [%s] %s' % (self.pk, self.name)


        

    
    
    


        
