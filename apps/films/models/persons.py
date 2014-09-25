# coding: utf-8

import os

from django.db import models
from ..constants import APP_PERSON_PHOTO_DIR
from utils.common import get_image_path
from apps.films.models.photoclass import PhotoClass


#############################################################################################################
# Модель Персон
class Persons(PhotoClass):
    city      = models.ForeignKey('Cities', null=True, blank=True, verbose_name=u'Город', related_name='persons')
    name      = models.CharField(max_length=255, db_index=True, verbose_name=u'Имя')
    name_orig = models.CharField(max_length=255, db_index=True, verbose_name=u'Оригинальное имя')
    bio       = models.TextField(verbose_name=u'Биография')
    photo     = models.ImageField(upload_to=get_image_path, blank=True, null=True, verbose_name=u'Фото')
    birthdate = models.DateField(verbose_name=u'Дата дня рождения', null=True, blank=True)
    kinopoisk_id = models.IntegerField(unique=True)


    @property
    def get_upload_to(self):
        return APP_PERSON_PHOTO_DIR


    @property
    def get_full_name(self):
        full_name = u"{0} ({1})".format(self.name, self.name_orig)
        return full_name.strip()


    @property
    def get_path_to_photo(self):
        path_to_photo = ''
        if self.photo:
            path_to_photo = self.photo.storage.url(self.photo.name)
        return path_to_photo


    def __unicode__(self):
        return u'[%s] %s' % (self.pk, self.get_full_name)


    @classmethod
    def get_sorted_persons_by_name(cls, filter={}, offset=None, limit=None, *args, **kwargs):
        obj = cls.objects.filter(**filter).order_by('name')[slice(offset, limit)]

        return obj


    class Meta:
        # Имя таблицы в БД
        db_table = 'persons'
        app_label = 'films'
        verbose_name = u'Персона'
        verbose_name_plural = u'Персоны'

