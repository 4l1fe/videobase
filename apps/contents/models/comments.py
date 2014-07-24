# coding: utf-8

from django.db import models
from django.contrib.auth.models import User

from apps.users.models import UsersProfile
from apps.contents.constants import APP_CONTENTS_COMMENT_STATUS


#############################################################################################################
# Модель Комментариев
class Comments(models.Model):
    user       = models.ForeignKey(User, verbose_name=u'Пользователь', related_name='comments')
    content    = models.ForeignKey('Contents', verbose_name=u'Контент')
    text       = models.TextField(verbose_name=u'Tекст комментария')
    parent_id  = models.IntegerField(null=True, blank=True, verbose_name=u'Родительский комментарий')
    status     = models.PositiveIntegerField(null=True, blank=True, choices=APP_CONTENTS_COMMENT_STATUS, verbose_name=u'Статус')
    created    = models.DateTimeField(auto_now_add=True, verbose_name=u'Создан')


    def __unicode__(self):
        return u'[{0}] {1} ({2})'.format(self.pk, self.user, self.content)

    class Meta:
        # Имя таблицы в БД
        db_table = 'comments'
        app_label = 'contents'
        verbose_name = u'Комментарий'
        verbose_name_plural = u'Комментарии'
