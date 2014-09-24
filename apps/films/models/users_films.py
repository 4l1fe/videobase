# coding: utf-8

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

from apps.films.constants import APP_USERFILM_STATUS, APP_USERFILM_STATUS_UNDEF, \
                                 APP_USERFILM_SUBS_FALSE, APP_USERFILM_SUBS, APP_USERFILM_SUBS_TRUE


#############################################################################################################
# Модель Пользовательских фильмов
class UsersFilms(models.Model):
    user       = models.ForeignKey(User, verbose_name=u'Идентификатор пользоваля', related_name='uf_users_rel')
    film       = models.ForeignKey('Films', verbose_name=u'Фильм', related_name='uf_films_rel')
    status     = models.PositiveSmallIntegerField(null=True, blank=True, db_index=True, default=APP_USERFILM_STATUS_UNDEF, choices=APP_USERFILM_STATUS, verbose_name=u'Статус фильма с т.з. пользователя')
    rating     = models.PositiveSmallIntegerField(null=True, blank=True, db_index=True, verbose_name=u'Рейтинг фильма поставленный пользователем')
    subscribed = models.PositiveSmallIntegerField(null=True, blank=True, default=APP_USERFILM_SUBS_FALSE, choices=APP_USERFILM_SUBS, verbose_name=u'Статус подписки')
    created    = models.DateTimeField(auto_now_add=True, verbose_name=u'Дата создания')


    def __unicode__(self):
        return u'[{0}] {1} - {2} ({3})'.format(self.pk, self.user.username, self.film.name, self.status)


    @property
    def check_subscribed(self):
        return False if self.subscribed == APP_USERFILM_SUBS_FALSE else True


    @property
    def get_name_status(self):
        return dict(APP_USERFILM_STATUS).get(self.status)


    @property
    def relation_for_vb_film(self):
        return {
            'subscribed': self.check_subscribed,
            'status': self.get_name_status if not self.status is None else None,
            'rating': self.rating,
        }


    @classmethod
    def get_subscribed_films_by_user(self, user_id, flat=False, *args, **kwargs):
        result = self.objects.filter(user=user_id, subscribed=APP_USERFILM_SUBS_TRUE).order_by('created')
        if flat:
            result = result.values_list('film', flat=True)

        return result


    class  Meta(object):
        # Имя таблицы в БД
        db_table = 'users_films'
        app_label = 'films'
        unique_together = (('user', 'film'),)
        verbose_name = u'Фильмы пользователя'
        verbose_name_plural = u'Фильмы пользователей'
