# coding: utf-8

from django.db import models
from django.contrib.auth.models import User

from apps.films.constants import APP_PERSONFILM_SUBS_FALSE, APP_PERSONFILM_SUBS, APP_PERSONFILM_SUBS_TRUE


#############################################################################################################
# Модель связи Пользователей и Персон
class UsersPersons(models.Model):
    user       = models.ForeignKey(User, max_length=255, verbose_name=u'Пользователь', related_name='persons')
    person     = models.ForeignKey('Persons', max_length=255, verbose_name=u'Персона', related_name='users_persons')
    upstatus   = models.IntegerField(verbose_name=u'Статус', default=0)
    subscribed = models.IntegerField(verbose_name=u'Подписка', default=APP_PERSONFILM_SUBS_FALSE, choices=APP_PERSONFILM_SUBS)
    created    = models.DateTimeField(auto_now_add=True, verbose_name=u'Дата создания')


    def __unicode__(self):
        return u'[%s %s]' % (self.user, self.person)

    @classmethod
    def get_subscribed_persons_by_user(self, user_id, flat=False):
        result = self.objects.filter(user=user_id, subscribed=APP_PERSONFILM_SUBS_TRUE).order_by('created')
        if flat:
            result = result.values_list('film', flat=True)

        return result


    class Meta:
        # Имя таблицы в БД
        db_table = 'users_persons'
        app_label = 'films'
        verbose_name = u'Персоны пользователя'
        verbose_name_plural = u'Персоны пользователей'
