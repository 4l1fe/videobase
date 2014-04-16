# coding: utf-8

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

from apps.films.constants import APP_USERFILM_STATUS, APP_USERFILM_STATUS_UNDEF, \
                                 APP_USERFILM_SUBS_FALSE, APP_USERFILM_SUBS


#############################################################################################################
# Модель Пользовательских фильмов
class UsersFilms(models.Model):
    user       = models.ForeignKey(User, verbose_name=u'Идентификатор пользоваля', related_name='films')
    film       = models.ForeignKey('Films', verbose_name=u'Фильм')
    status     = models.PositiveSmallIntegerField(null=True, blank=True, default=APP_USERFILM_STATUS_UNDEF, choices=APP_USERFILM_STATUS, verbose_name=u'Статус фильма с т.з. пользователя')
    rating     = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=u'Рейтинг фильма поставленный пользователем')
    subscribed = models.PositiveSmallIntegerField(null=True, blank=True, default=APP_USERFILM_SUBS_FALSE, choices=APP_USERFILM_SUBS, verbose_name=u'Статус подписки')


    def __unicode__(self):
        return u'[{0}] {1} - {2} ({3})'.format(self.pk, self.user.username, self.film.name, self.status)

    class  Meta(object):
        # Имя таблицы в БД
        db_table = 'users_films'
        app_label = 'films'
        unique_together = (('user', 'film'),)
        verbose_name = u'Фильмы пользователя'
        verbose_name_plural = u'Фильмы пользователей'
