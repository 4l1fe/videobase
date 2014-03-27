# coding: utf-8

from django.db import models
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

from ..constants import *


# class UserManager(BaseUserManager):
#     def create_user(self, email, password=None, **kwargs):
#         if not email:
#             raise ValueError('Users must have an email address')
#
#         user = self.model(email=UserManager.normalize_email(email), **kwargs)
#
#         user.set_password(password)
#         user.save(using=self._db)
#         return user


#############################################################################################################
# Модель Пользователей
class Users(models.Model):
    firstname    = models.CharField(max_length=255, verbose_name=u'Имя')
    lastname     = models.CharField(max_length=255, verbose_name=u'Фамилия')
    email        = models.EmailField(max_length=255, unique=True, verbose_name=u'Email')
    password     = models.CharField(max_length=255, verbose_name=u'Пароль')
    last_visited = models.DateTimeField(auto_now_add=True, verbose_name=u'Последний визит')
    created      = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=u'Дата создания')
    ustatus      = models.PositiveSmallIntegerField(choices=APP_USER_STATUS, verbose_name=u'Статус')
    userpic_type = models.CharField(null=True, blank=True, default=None, choices=APP_USER_PIC_TYPES, max_length=255, verbose_name=u'Тип картинки')
    userpic      = models.ForeignKey('UsersPics', default=None, null=True, blank=True, verbose_name=u'Аватар', related_name='+')
    is_staff     = models.BooleanField(default=True,null=False)
    is_admin     = models.BooleanField(default=False, null=False)

    # objects = UserManager()

    def __unicode__(self):
        return u'[%s] %s' % (self.pk, self.name)

    @property
    def name(self):
        """
        Get full name through a divider
        """
        full_name = u'%s %s' % (self.firstname, self.lastname)
        return full_name.strip()

    class Meta:
        # Имя таблицы в БД
        db_table = 'users'
        app_label = 'users'
        verbose_name = u'Пользователь'
        verbose_name_plural = u'Пользователи'
