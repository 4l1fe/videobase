# coding: utf-8
from django.db import models
from django.contrib.auth.models import User
from apps.casts.constants import CCU_STATUSES, CCU_OFFLINE


################################################################################
# Модель Пользовательских чатов трансляций
class CastsChatsUsers(models.Model):
    cast       = models.ForeignKey('Casts', verbose_name=u'Трансляция')
    blocked    = models.DateTimeField(auto_now_add=True, verbose_name=u'Время блокировки')
    user       = models.ForeignKey(User, verbose_name=u'Идентификатор пользоваля')
    status     = models.CharField(max_length=255, choices=CCU_STATUSES, default=CCU_OFFLINE, db_index=True, verbose_name=u'Статус')

    def __unicode__(self):
        return u'[{0}] {1} - {2}'.format(self.pk, self.user.username, self.cast.title)

    class Meta:
        # Имя таблицы в БД
        db_table = 'casts_chats_users'
        app_label = 'casts'
        verbose_name = u'Чат трансляции пользователя'
        verbose_name_plural = u'Чаты трансляций пользователей'
