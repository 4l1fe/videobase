# coding: utf-8

import sha
import uuid
import datetime

from django.db import models
from django.contrib.auth.models import User

from apps.users.constants import TYPE_PASSWD_HASH


class UsersHash(models.Model):
    user      = models.ForeignKey(User, verbose_name=u'Пользователь')
    hash_key  = models.CharField(max_length=255, editable=False, unique=True, verbose_name=u'Хеш')
    hash_type = models.CharField(choices=TYPE_PASSWD_HASH, max_length=255, editable=False, verbose_name=u'Хеш тип')
    activated = models.BooleanField(default=False, verbose_name=u'Использован')
    created   = models.DateTimeField(auto_now=True, editable=False, verbose_name=u'Дата создания')
    expired   = models.DateTimeField(editable=False, verbose_name=u'Дата истечения')

    def __unicode__(self):
        return u'[{0}] {1}'.format(self.user.id, self.hash_key)

    def generate_hash(self, user_id):
        salt = '{0}_{1}'.format(uuid.uuid4(), user_id)
        return sha.new(salt).hexdigest()

    @classmethod
    def get_by_hash(cls, hash_key, hash_type=None, **kwargs):
        curr_date = datetime.datetime.now()
        filter_param = {
            'hash_key': hash_key,
            'expired__gt': curr_date,
            'created__lt': curr_date,
            'activated': False
        }

        if not hash_type is None:
            if not isinstance(hash_type, (list, tuple)):
                hash_type = [hash_type]

            filter_param.update({'hash_type__in': hash_type})

        try:
            return cls.objects.get(**filter_param)
        except Exception, e:
            pass

        return None

    @classmethod
    def activate_key(cls):
        cls.activated = True
        cls.user.profile = True

        return cls

    def save(self, *args, **kwargs):
        if self.id is None:
            self.hash_key = self.generate_hash(self.user_id)
            self.expired = datetime.datetime.now() + datetime.timedelta(days=1)

        super(UsersHash, self).save(*args, **kwargs)

    class Meta:
        db_table = 'users_hash'
        app_label = 'users'
        verbose_name = u'Хеш пользователя'
        verbose_name_plural = u'Хеши пользователей'
