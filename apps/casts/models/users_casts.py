# coding: utf-8
from django.db import models
from django.contrib.auth.models import User


################################################################################
# Модель Пользовательских трансляций
class UsersCasts(models.Model):
    user       = models.ForeignKey(User, verbose_name=u'Идентификатор пользоваля')
    cast       = models.ForeignKey('Casts', verbose_name=u'Трансляция')
    rating     = models.PositiveSmallIntegerField(null=True, blank=True, db_index=True, verbose_name=u'Рейтинг поставленный пользователем')
    subscribed = models.DateTimeField(null=True, blank=True, verbose_name=u'Дата создания')

    def __unicode__(self):
        return u'[{0}] {1} - {2}'.format(self.pk, self.user.username, self.cast.title)

    class Meta:
        # Имя таблицы в БД
        db_table = 'users_casts'
        app_label = 'casts'
        unique_together = (('user', 'cast'),)
        verbose_name = u'Трансляции пользователя'
        verbose_name_plural = u'Трансляции пользователей'
