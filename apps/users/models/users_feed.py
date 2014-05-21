# coding: utf-8

from django.contrib.auth.models import User
from django.db import models

from apps.users.constants import APP_FEED_TYPE


class Feed(models.Model):
    """
    Содержит имена полей, которые переопределяют питоновские стандартные объекты.
    """
        
    user = models.ForeignKey(User, verbose_name="Пользователь", null=True, blank=True)
    created = models.DateTimeField(verbose_name="Дата создания", auto_now=True)
    type = models.CharField(verbose_name="Тип связанного объекта", choices=APP_FEED_TYPE, max_length=255, name='type')
    object = models.TextField(verbose_name="Связанный объект", name='object')
    text = models.TextField(verbose_name="Текст")

    class Meta:
        db_table = 'users_feed'
        app_label = 'users'
        verbose_name = u'Лента событий'
        verbose_name_plural = u'Ленты событий'
