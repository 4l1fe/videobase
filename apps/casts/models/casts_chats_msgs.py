# coding: utf-8

from django.db import models
from django.contrib.auth.models import User


#############################################################################################################
# Модель Сообщения пользовотеля в чате трансляции
class CastsChatsMsgs(models.Model):
    cast    = models.ForeignKey('Casts', verbose_name=u'Идентификатор пользоваля')
    created = models.DateTimeField(auto_now_add=True, verbose_name=u'Создан')
    user    = models.ForeignKey(User, verbose_name=u'Идентификатор пользоваля')
    text    = models.TextField(verbose_name=u"Код встраивания", blank=True, null=True)

    def __unicode__(self):
        return u'[{0}] {1} - {2}'.format(self.pk, self.user.username, self.cast.title)

    class Meta:
        # Имя таблицы в БД
        db_table = 'casts_chats_msgs'
        app_label = 'casts'
        verbose_name = u'Сообщение в чате трансляции'
        verbose_name_plural = u'Сообщения в чатах трансляций'
