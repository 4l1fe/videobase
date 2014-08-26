# coding: utf-8

from django.db import models


#############################################################################################################
# Модель Расширения персоны
class PersonsExtras(models.Model):
    person      = models.ForeignKey('Persons', max_length=255, verbose_name=u'Персона')
    etype       = models.CharField(max_length=255, db_index=True, verbose_name=u'')
    name        = models.TextField(verbose_name=u'Имя')
    name_orig   = models.TextField(verbose_name=u'Оригинальное имя')
    description = models.TextField(verbose_name=u'Описание')
    url         = models.CharField(max_length=255, verbose_name=u'Фото')

    
    def __unicode__(self):
        return u'[%s] %s' % (self.pk, self.person.get_full_name)


    class Meta:
        # Имя таблицы в БД
        db_table = 'persons_extras'
        app_label = 'films'
        verbose_name = u'Расширения персоны'
        verbose_name_plural = u'Расширения персон'
