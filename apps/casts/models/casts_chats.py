# coding: utf-8
from django.db import models


#############################################################################################################
# Модель Чатов Трансляций
class CastsChats(models.Model):
    cast   = models.OneToOneField('Casts', verbose_name=u'Трансляция')
    status = models.IntegerField(verbose_name=u'Статус')

    def __unicode__(self):
        return u'[{0}] {1} - {2}'.format(self.pk, self.cast, self.status)

    class Meta:
        # Имя таблицы в БД
        db_table = 'casts_chats'
        app_label = 'casts'
        verbose_name = u'Чат трансляции '
        verbose_name_plural = u'Чаты трансляций'
