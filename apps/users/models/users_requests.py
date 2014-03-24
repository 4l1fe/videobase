# coding: utf-8

from django.db import models


#############################################################################################################
# Модель Пользовательских запросов
class UsersRequests(models.Model):
    user    = models.ForeignKey('Users', verbose_name=u'Пользователи')
    hash    = models.IntegerField(verbose_name=u'Запрос')
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=u'Дата создания')
    rtype   = models.CharField(max_length=255, verbose_name=u'Тип запроса')
    value   = models.CharField(max_length=255, verbose_name=u'Значение запроса')


    def __unicode__(self):
        return u'[%s] %s' % (self.pk, self.user.name)

    class Meta:
        # Имя таблицы в БД
        db_table = 'users_requests'
        app_label = 'Users'
        verbose_name = u'Запросы пользователя'
        verbose_name_plural = u'Запросы пользователей'
