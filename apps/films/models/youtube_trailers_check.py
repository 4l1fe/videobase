# coding: utf-8

from django.db import models


class YoutubeTrailerCheck(models.Model):
    film            = models.ForeignKey('Films', verbose_name=u'Film')
    last_check      = models.DateTimeField(verbose_name=u'Last try datetime')
    was_successfull = models.BooleanField(default=False, verbose_name=u'Was finding a trailer succesfull')


    class Meta(object):
        # Имя таблицы в БД
        db_table = 'youtube_trailer_check'
        app_label = 'films'
        verbose_name = u'Youtube try'
        verbose_name_plural = u'Youtube tries'
