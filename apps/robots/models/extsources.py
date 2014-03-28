# coding: utf-8

from django.db import models


#############################################################################################################
# Модель Кинопоиска
class ExternalSources(models.Model):

    domain  = models.URLField(max_length = 255, verbose_name =u'Доменное имя', primary_key = True)


    def __unicode__(self):
        return u'[{0}] {1}'.format(self.pk, self.domain)

    class Meta:
        # Имя таблицы в БД
        db_table = 'robots_extsources'
        app_label = 'robots'
        verbose_name = u'Внешние источники'
        verbose_name_plural = u'Внешние источники'

