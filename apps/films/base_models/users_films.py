# coding: utf-8

from django.db import models


#############################################################################################################
# Модель Пользовательских фильмов
class UsersFilms(models.Model):
    user       = models.ForeignKey('Users', verbose_name=u'Идентификатор пользоваля')
    film       = models.ForeignKey('Films', verbose_name=u'Фильм')
    ufstatus   = models.IntegerField(verbose_name=u'Статус фильма с т.з. пользователя')
    ufrating   = models.IntegerField(verbose_name=u'Рейтинг фильма поставленный пользователем')
    subscribed = models.IntegerField(verbose_name=u'Статус подписки')


    def __unicode__(self):
        return u'[{0}] {1} - {2} ({3})'.format(self.pk, self.user.name, self.film.name, self.ufstatus)

    class  Meta(object):
        # Имя таблицы в БД
        db_table = 'users_films'
        app_label = 'Films'
        verbose_name = u'Фильмы пользователя'
        verbose_name_plural = u'Фильмы пользователей'
