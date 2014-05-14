# coding: utf-8

import os
import datetime
import binascii

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


################################################################################
# Модель сессий для доступа через API
class SessionToken(models.Model):
    """
    The default authorization token model.
    """
    user    = models.ForeignKey(User, verbose_name=u'Пользователь')
    key     = models.CharField(max_length=40, primary_key=True, verbose_name=u'Ключ')
    created = models.DateTimeField(auto_now_add=True, verbose_name=u'Дата создания')

    def __unicode__(self):
        return "[{0}]: {1}".format(self.user.pk, self.key)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20))

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()

        return super(SessionToken, self).save(*args, **kwargs)

    class Meta:
        # Имя таблицы в БД
        db_table = 'users_api_session_tokens'
        app_label = 'users'
        verbose_name = u'API сессия'
        verbose_name_plural = u'API Сессии'


class UsersApiSessions(models.Model):
    token   = models.ForeignKey(SessionToken, verbose_name=u'Токен')
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=u'Дата создания')
    active  = models.BooleanField(verbose_name=u'Активность сэссии', default=True)

    def __unicode__(self):
        return u'[{0}]: {1}'.format(self.pk, self.token)

    def get_expire_time(self):
        pass

    def get_expiration_time(self):
        return self.created + datetime.timedelta(minutes=settings.API_SESSION_EXPIRATION_TIME)

    class Meta:
        # Имя таблицы в БД
        db_table = 'users_api_sessions'
        app_label = 'users'
        verbose_name = u'API сессия'
        verbose_name_plural = u'API Сессии'
