# coding: utf-8

from django.db import models
from apps.users.models import Users


#############################################################################################################
# Модель связи Пользователей и Персон
class UsersPersons(models.Model):
    user       = models.ForeignKey(Users, max_length=255, verbose_name=u'Пользователь')
    person     = models.ForeignKey('Persons', max_length=255, verbose_name=u'Персона')
    upstatus   = models.IntegerField(verbose_name=u'Статус')
    subscribed = models.IntegerField(verbose_name=u'Подписка')


    def __unicode__(self):
        return u'[%s %s]' % (self.user, self.person)

    class Meta:
        # Имя таблицы в БД
        db_table = 'users_persons'
        app_label = 'films'
        verbose_name = u'Персоны пользователя'
        verbose_name_plural = u'Персоны пользователей'
