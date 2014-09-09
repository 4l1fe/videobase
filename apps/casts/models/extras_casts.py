# coding: utf-8

from django.db import models
from django.contrib.auth.models import User

from django.core.validators import MaxValueValidator, MinValueValidator

from apps.films.models import FilmExtras



#############################################################################################################
# Модель Пользовательских трансляций
class CastsExtras(models.Model):
    cast       = models.ForeignKey('Casts', verbose_name=u'Идентификатор пользоваля')
    extra      = models.ForeignKey(FilmExtras, verbose_name=u'Extra')


    def __unicode__(self):
        return u'[{0}] {1} - {2}'.format(self.pk, self.cast.title, self.extra)

        
    class  Meta(object):
        # Имя таблицы в БД
        db_table = 'extras_casts'
        app_label = 'casts'
        verbose_name = u'Трансляции extra'
        verbose_name_plural = u'Трансляции extra'
        
