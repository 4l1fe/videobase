# coding: utf-8

from django.db import models


#############################################################################################################
# Модель Пользовательских логов
class UsersLogs(models.Model):
    user    = models.ForeignKey('Users', verbose_name=u'Пользователи')
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=u'Дата создания')
    itype   = models.CharField(max_length=255, verbose_name=u'Тип')
    iobject = models.CharField(max_length=255, verbose_name=u'Объект')
    itext   = models.CharField(max_length=255, verbose_name=u'Текст')

    def __unicode__(self):
        return u'[%s] %s' % (self.pk, self.user.name)

    class Meta:
        # Имя таблицы в БД
        db_table = 'users_logs'
        app_label = 'Users'
        verbose_name = u'Лог пользователя'
        verbose_name_plural = u'Логи пользователей'
