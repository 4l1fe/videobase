# coding: utf-8
from django.contrib.auth.models import User
from django.db import models

from ..constants import *


class UsersProfile(models.Model):
    user         = models.OneToOneField(User, verbose_name=u'Пользователь', related_name='profile')
    last_visited = models.DateTimeField(verbose_name=u'Песледний визит', auto_now_add=True, blank=True)
    userpic_id   = models.IntegerField(verbose_name=u'Id аватарки', null=True, blank=True)

    # Notification
    ntf_vid_new        = models.BooleanField(verbose_name=u'Появление нового фильма', default=True)
    ntf_vid_director   = models.BooleanField(verbose_name=u'Появление фильма с персоной', default=True)
    ntf_frnd_rate      = models.BooleanField(verbose_name=u'Новая оценка друзей', default=True)
    ntf_frnd_comment   = models.BooleanField(verbose_name=u'Новый коментарий друзей', default=True)
    ntf_frnd_subscribe = models.BooleanField(verbose_name=u'Новая подписка друзей', default=True)
    ntf_frequency      = models.IntegerField(verbose_name=u'Частота уведомлений', choices=APP_USERPROFILE_NOTIFICATION, default=APP_USERPROFILE_NOTIFICATION_DAY)

    # Privacy
    pvt_subscribes = models.IntegerField(verbose_name=u'Подписки пользователя', choices=APP_USERPROFILE_PRIVACY, default=APP_USERPROFILE_PRIVACY_ALL)
    pvt_friends    = models.IntegerField(verbose_name=u'Друзья пользователя', choices=APP_USERPROFILE_PRIVACY, default=APP_USERPROFILE_PRIVACY_ALL)
    pvt_genres     = models.IntegerField(verbose_name=u'Любимые жанры пользователя', choices=APP_USERPROFILE_PRIVACY, default=APP_USERPROFILE_PRIVACY_ALL)
    pvt_actors     = models.IntegerField(verbose_name=u'Любимые актеры пользователя', choices=APP_USERPROFILE_PRIVACY, default=APP_USERPROFILE_PRIVACY_ALL)
    pvt_directors  = models.IntegerField(verbose_name=u'Любимые режисеры пользователя', choices=APP_USERPROFILE_PRIVACY, default=APP_USERPROFILE_PRIVACY_ALL)

    def __unicode__(self):
        return u'[%s] %s' % (self.id, self.user.username, )

    def get_name(self):
        return self.user.first_name

    class Meta:
        db_table = 'users_profile'
        app_label = 'users'
        verbose_name = u'Профиль пользователя'
        verbose_name_plural = u'Профили пользователей'
