# coding: utf-8

import os
import datetime
import binascii

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User

from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions

from utils.common import get_authorization_header


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


class MultipleTokenAuthentication(BaseAuthentication):
    """
    A custom token model may be used, but must have the following properties.

    * key -- The string identifying the token
    * user -- The user to which the token belongs
    """

    model = SessionToken

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != b'x-vb-token':
            return None

        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid token header. Token string should not contain spaces.'
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(auth[1])

    def authenticate_credentials(self, key):
        try:
            token = self.model.objects.get(key=key)
        except self.model.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted')

        try:
            uas = UsersApiSessions.objects.get(token=token)

            if uas.get_expiration_time() < timezone.now():
                raise exceptions.AuthenticationFailed('Session expired')

        except UsersApiSessions.DoesNotExist:
            raise exceptions.AuthenticationFailed('There is no session associated with this token')

        return token.user, token

    def authenticate_header(self, request):
        return 'X-VB-Token'


class UsersApiSessions(models.Model):
    token   = models.ForeignKey(SessionToken, verbose_name=u'Токен')
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=u'Дата создания')


    def __unicode__(self):
        return u'[{0}]: {1}'.format(self.pk, self.user.name)

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
