# coding: utf-8

from django.db import models
from ..constants import *

################################################################################
# модель Пользовательских отношений
class UsersRels(models.Model):
    user = models.ForeignKey('Users', verbose_name=u'Пользователи')
    user_rel = models.ForeignKey('Users', related_name='user_rel',verbose_name=u'Пользователи')
    rel_type = models.CharField(max_length=255,
                                choices=REL_TYPES,
                                verbose_name=u'Тип отношений')
    updated = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=u'Дата создания/обновления')

    def __unicode__(self):
        return u'[%s] %s' % (self.pk, self.user.name)

    class Meta:
        # Имя таблицы в БД
        db_table = 'users_rels'
        verbose_name = u'Отношения пользователей'
        verbose_name_plural = u'Отношения пользователей'
