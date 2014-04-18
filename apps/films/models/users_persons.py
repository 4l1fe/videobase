# coding: utf-8

from django.db import models
from django.contrib.auth.models import User


#############################################################################################################
# Модель связи Пользователей и Персон
class UsersPersons(models.Model):
    user       = models.ForeignKey(User, max_length=255, verbose_name=u'Пользователь', related_name='persons')
    person     = models.ForeignKey('Persons', max_length=255, verbose_name=u'Персона', related_name='users_persons')
    upstatus   = models.IntegerField(verbose_name=u'Статус', default=0)
    subscribed = models.IntegerField(verbose_name=u'Подписка', default=0)

    def __unicode__(self):
        return u'[%s %s]' % (self.user, self.person)

    class Meta:
        # Имя таблицы в БД
        db_table = 'users_persons'
        app_label = 'films'
        verbose_name = u'Персоны пользователя'
        verbose_name_plural = u'Персоны пользователей'
