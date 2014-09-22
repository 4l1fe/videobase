# coding: utf-8
import os
import datetime
import binascii

from django.utils import timezone
from django.db import models

from apps.users.models import User
from videobase.settings import SESSION_EXPIRATION_TIME


class SessionToken(models.Model):
    key       = models.CharField(verbose_name=u'Токен', primary_key=True, max_length=40)
    user      = models.ForeignKey(User, verbose_name=u'Пользователь', related_name='session')
    created   = models.DateTimeField(verbose_name=u'Дата создания', auto_now_add=True, editable=False)
    updated   = models.DateTimeField(verbose_name=u'Время обновления', auto_now_add=True)
    is_active = models.BooleanField(verbose_name=u'Активность сэссии', default=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(SessionToken, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20))

    def get_expiration_time(self):
        return self.updated + SESSION_EXPIRATION_TIME

    @classmethod
    def get_user(cls, key):
        try:
            session = cls.objects.get(key=key)
        except cls.DoesNotExist:
            return None
        if session.get_expiration_time() <= timezone.now():
            return session.user
        return None

    def __unicode__(self):
        return u'[{0}]: {1}'.format(self.pk, self.key)

    class Meta:
        # Имя таблицы в БД
        db_table = 'session_token'
        app_label = 'users'
        ordering = ('updated', )
        verbose_name = u'Токен сессии'
        verbose_name_plural = u'Токены сессии'
