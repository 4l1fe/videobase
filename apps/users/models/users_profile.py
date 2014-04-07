# coding: utf-8
from django.contrib.auth.models import User
from django.db import models

from ..constants import *


class UsersProfile(models.Model):
    user         = models.OneToOneField(User, verbose_name=u'Пользователь', related_name='profile')
    last_visited = models.DateTimeField(verbose_name=u'Песледний визит', auto_now_add=True, blank=True)
    created      = models.DateTimeField(verbose_name=u'Время создания', auto_now_add=True, blank=True)
    status       = models.SmallIntegerField(verbose_name=u'Статус пользователя', choices=APP_USER_STATUS, default=APP_USER_ACTIVE)
    userpic_type = models.CharField(max_length=255, verbose_name=u'Тип', choices=APP_USER_REL_TYPES, null=True, blank=True)
    userpic_id   = models.IntegerField(verbose_name=u'Id аватарки', null=True, blank=True)

    class Meta:
        db_table = 'users_profile'
        app_label = 'users'
        verbose_name = u'Профиль пользователя'
        verbose_name_plural = u'Профили пользователей'
