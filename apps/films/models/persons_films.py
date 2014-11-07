# coding: utf-8

from django.db import models
from ..constants import *


#############################################################################################################
# Модель Роли персон в производстве фильмов
class PersonsFilms(models.Model):
    film        = models.ForeignKey('Films', verbose_name=u'Фильм', related_name="pf_films_rel")
    person      = models.ForeignKey('Persons', verbose_name=u'Персона', related_name='pf_persons_rel')
    p_type      = models.CharField(max_length=255, db_index=True, choices=APP_FILM_PERSON_TYPES, verbose_name=u'Тип персоны')
    p_index     = models.IntegerField(default=0, db_index=True, verbose_name=u'Порядок на кинопоиске')
    p_character = models.CharField(max_length=255, default='')
    description = models.CharField(max_length=255, default='')


    def __unicode__(self):
        return u'[{0}] {1} {2}'.format(self.pk, self.film.name, self.person.name)

    class  Meta(object):
        # Имя таблицы в БД
        db_table = 'persons_films'
        app_label = 'films'
        verbose_name = u'Роль персоны в производстве фильма'
        verbose_name_plural = u'Роли персон в производстве фильмов'
        unique_together = (('film', 'person', 'p_type'),)
