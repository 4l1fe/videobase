# coding: utf-8

from django.db import models
from django.contrib.auth.models import User

from ..constants import *


################################################################################
# Модель Пользовательских отношений
class UsersRels(models.Model):
    user = models.ForeignKey(User, verbose_name=u'Пользователи', related_name='rels')
    user_rel = models.ForeignKey(User, related_name='user_rel', verbose_name=u'Пользователи')
    rel_type = models.CharField(max_length=255, choices=APP_USER_REL_TYPES, verbose_name=u'Тип отношений')
    updated = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=u'Дата создания/обновления')

    def __unicode__(self):
        return u'[%s] %s - %s' % (self.pk, self.user.username, self.user_rel.username)

    class Meta:
        # Имя таблицы в БД
        db_table = 'users_rels'
        app_label = 'users'
        unique_together = ('user', 'user_rel', )
        verbose_name = u'Отношения пользователей'
        verbose_name_plural = u'Отношения пользователей'
