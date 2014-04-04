# coding: utf-8

from django.db import models

from apps.users.models import Users


#############################################################################################################
# Модель Комментариев
class Comments(models.Model):
    user       = models.ForeignKey(Users, verbose_name=u'Пользователь')
    content    = models.IntegerField(verbose_name=u'Контент')
    text       = models.TextField(verbose_name=u'Tекст комментария')
    parent_id  = models.IntegerField(verbose_name=u'Родительский комментарий')
    status     = models.CharField(max_length=40, verbose_name=u'Статус')
    created    = models.DateTimeField(auto_now_add=True, verbose_name=u'Создан')


    def __unicode__(self):
        return u'[{0}] {1} ({2})'.format(self.pk, self.user.name, self.content)

    class Meta:
        # Имя таблицы в БД
        db_table = 'comments'
        app_label = 'contents'
        verbose_name = u'Комментарий'
        verbose_name_plural = u'Комментарии'
