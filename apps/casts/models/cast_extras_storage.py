# coding: utf-8
import os
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.query import QuerySet
from apps.films.models.photoclass import PhotoClass
from apps.casts.constants import APP_CAST_POSTER_DIR
from utils.common import get_image_path
import videobase.settings as settings

# Модель Расширения фильмов/сериалов
class CastExtrasStorage(PhotoClass):
    cast        = models.ForeignKey('Casts', verbose_name=u'Cast', related_name="ce_cast_rel")
    name        = models.CharField(max_length=255, verbose_name=u'Название')
    name_orig   = models.CharField(max_length=255, verbose_name=u'Оригинальное название')
    photo       = models.ImageField(upload_to=get_image_path, blank=True, null=True, verbose_name=u'Постер')

    def __init__(self, *args, **kwargs):
        super(CastsExtrasStorage, self).__init__(*args, **kwargs)
        self._original_type = self.type


    @property
    def get_upload_to(self):
        return APP_CAST_POSTER_DIR

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
        db_table = 'casts_extras'
        app_label = 'casts'
        verbose_name = u'Дополнительный материал к cast'
        verbose_name_plural = u'Дополнительные материалы к cast'

