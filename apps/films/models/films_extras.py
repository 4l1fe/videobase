# coding: utf-8

from django.db import models
from ..constants import *
from apps.films.models.photoclass import PhotoClass
from utils.common import get_image_path


#############################################################################################################
# Модель Расширения фильмов/сериалов
class FilmExtras(PhotoClass):
    film        = models.ForeignKey('Films', verbose_name=u'Фильм')
    etype       = models.CharField(max_length=255, choices=APP_FILM_TYPE_ADDITIONAL_MATERIAL,
                                   verbose_name=u'Тип дополнительного материала')
    name        = models.CharField(max_length=255, verbose_name=u'Название')
    name_orig   = models.CharField(max_length=255, verbose_name=u'Оригинальное название')
    description = models.TextField(verbose_name=u'Описание')
    url         = models.URLField(max_length=255, verbose_name=u'Ссылка на дополнительный материал')
    photo       = models.ImageField(upload_to=get_image_path, blank=True, null=True, verbose_name=u'Постер')


    @property
    def get_upload_to(self):
        return APP_FILM_POSTER_DIR


    def __unicode__(self):
        return u'[{0}] {1}'.format(self.pk, self.name)

    class  Meta(object):
        # Имя таблицы в БД
        db_table = 'films_extras'
        app_label = 'films'
        verbose_name = u'Дополнительный материал к фильму'
        verbose_name_plural = u'Дополнительные материалы к фильмам'
