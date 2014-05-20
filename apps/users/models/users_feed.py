# coding=utf-8
from django.contrib.auth.models import User
from django.db import models


class Feed(models.Model):
    """Содержит имена полей, которые переопределяют питоновские стандартные объекты.
    """
    user = models.ForeignKey(User)
    created = models.DateField(auto_now_add=True)
    type = models.CharField(max_length=255, name='type')
    object = models.TextField(name='object')
    text = models.TextField()

    class Meta:
        db_table = 'users_feed'
        app_label = 'users'
        verbose_name = u'Лента событий'
        verbose_name_plural = u'Ленты событий'