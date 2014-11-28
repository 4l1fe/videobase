# coding: utf-8

__author__ = 'vladimir'

from django.db import models

# Модель Список рассылки для роботов
class RobotsMailList(models.Model):
    email = models.CharField(max_length=255, verbose_name=u'Email')

    def __unicode__(self):
        return u'[{0}] {1}'.format(self.pk, self.email,)

    class Meta:
        # Имя таблицы в БД
        db_table = 'robots_mail_list'
        app_label = 'robots'
        verbose_name = u'Список рассылки для робота'
        verbose_name_plural = u'Список рассылки для роботов'
