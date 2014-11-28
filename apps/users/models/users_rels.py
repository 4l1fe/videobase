# coding: utf-8

from django.db import models
from django.contrib.auth.models import User

from apps.users.constants import APP_USER_REL_TYPE_FRIENDS, APP_USER_REL_TYPES


################################################################################
# Модель Пользовательских отношений
class UsersRels(models.Model):
    user = models.ForeignKey(User, verbose_name=u'Пользователи', related_name='rels')
    user_rel = models.ForeignKey(User, related_name='user_rel', verbose_name=u'Пользователи')
    rel_type = models.CharField(max_length=255, choices=APP_USER_REL_TYPES, verbose_name=u'Тип отношений')
    updated = models.DateTimeField(auto_now=True, editable=False, verbose_name=u'Дата создания/обновления')

    def __unicode__(self):
        return u'[%s] %s - %s' % (self.pk, self.user.username, self.user_rel.username)

    @classmethod
    def get_all_friends_user(self, user_id, flat=False):
        result = self.objects.filter(rel_type=APP_USER_REL_TYPE_FRIENDS, user=user_id)
        if flat:
            result = result.values_list('user_rel', flat=True)

        return result

    def save(self, *args, **kwargs):
        if self.user != self.user_rel:
            super(UsersRels, self).save(*args, **kwargs)
        else:
            raise ValueError('Связь к самому себе')

    class Meta:
        # Имя таблицы в БД
        db_table = 'users_rels'
        app_label = 'users'
        unique_together = ('user', 'user_rel', )
        verbose_name = u'Отношения пользователей'
        verbose_name_plural = u'Отношения пользователей'
