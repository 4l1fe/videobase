# coding: utf-8

from django.db import models











#############################################################################################################
# Пользователи
class Users(models.Model):
    firstname    = models.CharField(max_length=255, verbose_name=u'Имя')
    lastname     = models.CharField(max_length=255, verbose_name=u'Фамилия')
    email        = models.EmailField(max_length=255, verbose_name=u'Email')
    passhash     = models.CharField(max_length=255, verbose_name=u'Пароль')
    last_visited = models.DateTimeField(verbose_name=u'Последний визит')
    created      = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=u'Дата создания')
    ustatus      = models.PositiveSmallIntegerField(verbose_name=u'Статус')
    userpic_type = models.CharField(max_length=255, verbose_name=u'Тип картинки')
    userpic_id   = models.IntegerField(verbose_name=u'ID картинки')


    def __unicode__(self):
        return u'[%s] %s %s' % (self.pk, self.firstname, self.lastname)

    class Meta:
        # Имя таблицы в БД
        db_table = 'users'
        verbose_name = u'Пользователь'
        verbose_name_plural = u'Пользователи'