# coding: utf-8

from django.db import models

# Create your models here.
class Users(models.Model):
    firstname = models.CharField(max_length=255, verbose_name=u'')
    lastname  = models.CharField(max_length=255, verbose_name=u'')
    email     = models.EmailField(max_length=255, verbose_name=u'')
    passhash  = models.CharField(max_length=255, verbose_name=u'')
    last_visited = models.DateTimeField(verbose_name=u'')
    created   = models.DateTimeField(verbose_name=u'')
    ustatus   = models.PositiveSmallIntegerField(verbose_name=u'')
    userpic_type = models.CharField(max_length=255, verbose_name=u'')
    userpic_type = models.IntegerField(verbose_name=u'')


    def __unicode__(self):
        return u'[%s] %s %s' % (self.pk, self.firstname, self.lastname)

    class Meta:
        # Имя таблицы в БД
        db_table = 'users'
        verbose_name = u'Пользователь'
        verbose_name_plural = u'Пользователи'