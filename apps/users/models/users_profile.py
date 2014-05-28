# coding: utf-8
from django.contrib.auth.models import User
from django.db import models
from users_pics import UsersPics

from ..constants import *


class UsersProfile(models.Model):
    user         = models.OneToOneField(User, verbose_name=u'Пользователь', related_name='profile')
    nickname     = models.CharField(max_length=128, verbose_name=u'Имя пользователя', null=True, blank=True)
    last_visited = models.DateTimeField(verbose_name=u'Песледний визит', auto_now_add=True, blank=True)
    userpic_type = models.CharField(max_length=255, verbose_name=u'Тип', choices=APP_USER_PIC_TYPES, null=True, blank=True)
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
        return self.nickname or self.user.username

    def as_comment_vbUser(self):

        image = UsersPics.objects.get(id=self.userpic_id).image

        url = image.storage.url(image.name)
        return {'id': self.user.pk,
                'name': self.nickname,
                'avatar': url
                }

    class Meta:
        db_table = 'users_profile'
        app_label = 'users'
        verbose_name = u'Профиль пользователя'
        verbose_name_plural = u'Профили пользователей'
