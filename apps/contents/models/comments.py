# coding: utf-8

from django.db import models
from django.contrib.auth.models import User
from apps.users.models import UsersProfile


#############################################################################################################
# Модель Комментариев
class Comments(models.Model):
    user       = models.ForeignKey(User, verbose_name=u'Пользователь')
    content    = models.IntegerField(verbose_name=u'Контент')
    text       = models.TextField(verbose_name=u'Tекст комментария')
    parent_id  = models.IntegerField(verbose_name=u'Родительский комментарий')
    status     = models.CharField(max_length=40, verbose_name=u'Статус')
    created    = models.DateTimeField(auto_now_add=True, verbose_name=u'Создан')


    def as_vbComment(self):
        try:
            user_profile = UsersProfile.objects.get(user = self.user)
        except UsersProfile.DoesNotExist :
            raise NameError("UserProfile doesn't exist for this user")


        return {'user':user_profile.as_comment_vbUser(),
                'films': {self.content.film.name,
                          self.content.film.id},
                'text': self.text,
                'created': self.created
        }

    def __unicode__(self):
        return u'[{0}] {1} ({2})'.format(self.pk, self.user, self.content)

    class Meta:
        # Имя таблицы в БД
        db_table = 'comments'
        app_label = 'contents'
        verbose_name = u'Комментарий'
        verbose_name_plural = u'Комментарии'


