# coding: utf-8

import os

from django.db import models
from ..constants import APP_PERSON_PHOTO_DIR
from utils.common import get_image_path
from apps.films.models.photoclass import PhotoClass


#############################################################################################################
# Модель Персон
class Persons(PhotoClass):
    city_id   = models.ForeignKey('Cities', verbose_name=u'Город', related_name='persons')
    name      = models.CharField(max_length=255, verbose_name=u'Имя')
    name_orig = models.CharField(max_length=255, verbose_name=u'Оригинальное имя')
    bio       = models.TextField(verbose_name=u'Биография')
    photo     = models.ImageField(upload_to=get_image_path, blank=True, null=True, verbose_name=u'Фото')

    @property
    def get_upload_to(self):
        return APP_PERSON_PHOTO_DIR

    @property
    def get_full_name(self):
        full_name = u"{0} ({1})".format(self.name, self.name_orig)
        return full_name.strip()

    # @property
    # def birthplace(self):
    #     bp = (self.city_id.name, self.city_id.country_id.name)
    #     return bp


    def __unicode__(self):
        return u'[%s] %s' % (self.pk, self.get_full_name)

    def as_vBPerson(self, extend = False):

        p_dict ={'id': self.pk,
                'name': self.name,
                'photo': self.photo if self.photo else '',
        }
        if extend:
            p_dict['bio'] = self.bio
        return p_dict

        
    class Meta:
        # Имя таблицы в БД
        db_table = 'persons'
        app_label = 'films'
        verbose_name = u'Персона'
        verbose_name_plural = u'Персоны'
