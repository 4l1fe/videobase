# coding: utf-8

import os

from django.db import models
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS

from apps.films.constants import *
from apps.films.models.photoclass import PhotoClass
from apps.films.constants import APP_FILM_TYPE_ADDITIONAL_MATERIAL_POSTER, APP_FILM_TYPE_ADDITIONAL_MATERIAL_TRAILER


from utils.common import get_image_path

import videobase.settings as settings

#############################################################################################################
#
class PosterFilmManager(models.Manager):
    def get_query_set(self):
        return super(PosterFilmManager, self).get_query_set().filter(type=APP_FILM_TYPE_ADDITIONAL_MATERIAL_POSTER)

#############################################################################################################
# Модель Расширения фильмов/сериалов
class FilmExtras(PhotoClass):
    film        = models.ForeignKey('Films', verbose_name=u'Фильм', related_name="fe_film_rel")
    type        = models.CharField(max_length=255, choices=APP_FILM_TYPE_ADDITIONAL_MATERIAL, verbose_name=u'Тип дополнительного материала')
    name        = models.CharField(max_length=255, verbose_name=u'Название')
    name_orig   = models.CharField(max_length=255, verbose_name=u'Оригинальное название')
    description = models.TextField(verbose_name=u'Описание')
    url         = models.URLField(max_length=255, blank=True, null=True, verbose_name=u'Ссылка на дополнительный материал')
    photo       = models.ImageField(upload_to=get_image_path, blank=True, null=True, verbose_name=u'Постер')

    objects = models.Manager()
    poster_obj = PosterFilmManager()


    def __init__(self, *args, **kwargs):
        super(FilmExtras, self).__init__(*args, **kwargs)
        self._original_type = self.type


    @property
    def get_upload_to(self):
        return APP_FILM_POSTER_DIR


    def clean(self, *args, **kwargs):
        if not self.pk is None:
            if self._original_type != self.type:
                msg = {'type': (u"Это поле не изменяемо",)}
                raise ValidationError(msg)


    def save(self, *args, **kwargs):
        if self.type == APP_FILM_TYPE_ADDITIONAL_MATERIAL_POSTER:
            self.url = None
        elif self.type == APP_FILM_TYPE_ADDITIONAL_MATERIAL_TRAILER:
            self.photo = None

        super(FilmExtras, self).save(*args, **kwargs)


    @classmethod
    def get_additional_material_by_film(cls, ids):
        if not isinstance(ids, list):
            ids = [ids]

        return cls.objects.filter(film__in=ids, type=APP_FILM_TYPE_ADDITIONAL_MATERIAL_POSTER)


    @classmethod
    def get_trailer_by_film(cls, ids, first=False, *args, **kwargs):
        if not isinstance(ids, list):
            ids = [ids]

        result = cls.objects.filter(film__in=ids, type=APP_FILM_TYPE_ADDITIONAL_MATERIAL_TRAILER)
        if first:
            result = result.first()

        return result


    @classmethod
    def get_poster_by_film(cls, list_extras):
        poster = ''
        if not isinstance(list_extras, list):
            list_extras = [list_extras]

        for item in list_extras:
            if not item.photo is None and item.photo:
                poster = item.get_photo_url()
                break

        return poster


    def get_photo_url(self, prefix=True):
        result = ''
        if not self.photo is None and self.photo:
            result = list(os.path.splitext(self.photo.url))
            if prefix:
                result[0] += settings.POSTER_URL_PREFIX

            result = u''.join(result)

        return result


    def __unicode__(self):
        return u'[{0}] {1}'.format(self.pk, self.name)


    class  Meta(object):
        # Имя таблицы в БД
        db_table = 'films_extras'
        app_label = 'films'
        verbose_name = u'Дополнительный материал к фильму'
        verbose_name_plural = u'Дополнительные материалы к фильмам'
