# coding: utf-8

from django.db import models
from django.contrib.auth.models import User

from apps.users.models import UsersPics
from apps.contents.constants import APP_CONTENTS_COMMENT_STATUS


#############################################################################################################
# Модель Комментариев
class Comments(models.Model):
    user       = models.ForeignKey(User, verbose_name=u'Пользователь', related_name='comments')
    content    = models.ForeignKey('Contents', verbose_name=u'Контент')
    text       = models.TextField(verbose_name=u'Tекст комментария')
    parent_id  = models.IntegerField(null=True, blank=True, verbose_name=u'Родительский комментарий')
    status     = models.PositiveIntegerField(null=True, blank=True, choices=APP_CONTENTS_COMMENT_STATUS, verbose_name=u'Статус')
    created    = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name=u'Создан')

    def __unicode__(self):
        return u'[{0}] {1} ({2})'.format(self.pk, self.user, self.content)


    @classmethod
    def get_top_comments_with_rating(cls, struct=False, limit=12):
        sql = """
        SELECT comments.*, films.id AS film_id, films.name as name,
               users_films.rating as rating, auth_user.first_name as us_name,
               users_profile.userpic_id as user_pic
        FROM comments
        INNER JOIN content ON content.id = comments.content_id
        INNER JOIN users_films ON users_films.film_id = content.film_id AND comments.user_id = users_films.user_id
        LEFT JOIN films ON users_films.film_id = films.id
        LEFT JOIN auth_user ON comments.user_id = auth_user.id
        LEFT JOIN users_profile ON comments.user_id = users_profile.user_id

        WHERE users_films.rating IS NOT NULL AND users_films.rating > 0 and NOT auth_user.first_name = ''
        ORDER BY comments.created DESC LIMIT %s;
        """

        obj = cls.objects.raw(sql, [limit])
        if struct:
            return [{
                'film': {
                    'id': item.film_id,
                    'name': item.name,
                    'rating': item.rating,
                },
                'user': {
                    'id': item.user_id,
                    'name': item.us_name,
                    'avatar': '' if item.user_pic is None else UsersPics.get_picture(item.user_pic),
                },
                'text': item.text,
            } for item in obj]

        return obj

    @classmethod
    def get_comments_sorting_by_created(cls):
        return cls.objects.order_by("-created")[0:20]


    class Meta:
        # Имя таблицы в БД
        db_table = 'comments'
        app_label = 'contents'
        verbose_name = u'Комментарий'
        verbose_name_plural = u'Комментарии'
