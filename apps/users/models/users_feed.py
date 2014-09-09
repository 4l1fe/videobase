# coding: utf-8

from django.contrib.auth.models import User
from django.db import models

from apps.users.constants import APP_FEED_TYPE, APP_USERS_API_DEFAULT_PER_PAGE,\
                                 FILM_O, PERSON_O
import jsonfield


class Feed(models.Model):
    """
    Содержит имена полей, которые переопределяют питоновские стандартные объекты.
    """

    user = models.ForeignKey(User, verbose_name="Пользователь", null=True, blank=True)
    created = models.DateTimeField(verbose_name="Дата создания", auto_now=True)
    type = models.CharField(verbose_name="Тип связанного объекта", choices=APP_FEED_TYPE, max_length=255, name='type')
    obj_id = models.IntegerField(verbose_name='Идентификатор объекта', null=True, blank=True)
    child_obj_id = models.IntegerField(verbose_name='Идентификатор дочернего объекта', null=True, blank=True)
    text = models.TextField(verbose_name="Текст", null=True, blank=True)

    def __unicode__(self):
        return u"[{id}]{type}".format(id=self.pk, type=self.get_type_display())

    @classmethod
    def list_to_str(cls, arr):
        temp_str = "{}"
        try:
            if len(arr):
                temp_str = "{%s}" % ','.join(str(i) for i in arr)
        except:
            pass

        return temp_str

    @classmethod
    def get_feeds_by_user(cls, user_id, uf=[], up=[], offset=0, limit=APP_USERS_API_DEFAULT_PER_PAGE, count=False, *args, **kwargs):
        sql = """("users_feed"."user_id"=%s OR "users_feed"."user_id" IS NULL) AND (CASE
            WHEN "users_feed"."user_id" IS NULL AND "users_feed"."type"=%s THEN
              CAST(coalesce(obj_id, '0') AS integer)=ANY(%s::integer[])
            WHEN "users_feed"."user_id" IS NULL AND "users_feed"."type"=%s THEN
              CAST(coalesce(obj_id, '0') AS integer)=ANY(%s::integer[])
            ELSE true END)"""

        o_feed = cls.objects.extra(where=[sql],
                                   params=[user_id, FILM_O, cls.list_to_str(uf), PERSON_O, cls.list_to_str(up)])
        result = o_feed.order_by('-created')[offset:(limit + offset)]

        if count:
            return result, o_feed.count()

        return result

    @classmethod
    def get_feeds_by_user_friends(self, ur=[], count=False, offset=0, limit=APP_USERS_API_DEFAULT_PER_PAGE, *args, **kwargs):
        o_feed = self.objects.extra(
            where=['"users_feed"."user_id"=ANY(%s::integer[])'],
            params=[self.list_to_str(ur)]
        )
        result = o_feed.order_by('-created')[offset:(limit + offset)]

        if count:
            return result, o_feed.count()

        return result

    @classmethod
    def get_feeds_by_user_all(self, user_id, uf=[], up=[], ur=[], count=False, offset=0, limit=APP_USERS_API_DEFAULT_PER_PAGE, *args, **kwargs):
        sql = """("users_feed"."user_id"=ANY(%s::integer[]) OR "users_feed"."user_id" IS NULL) AND (CASE
            WHEN "users_feed"."user_id" IS NULL AND "users_feed"."type"=%s THEN
              CAST(coalesce(object->>'id', '0') AS integer)=ANY(%s::integer[])
            WHEN "users_feed"."user_id" IS NULL AND "users_feed"."type"=%s THEN
              CAST(coalesce(object->>'id', '0') AS integer)=ANY(%s::integer[])
            ELSE true END)
        """

        o_feed = self.objects.extra(
            where=[sql],
            params=[self.list_to_str(ur + [user_id]), FILM_O, self.list_to_str(uf), PERSON_O, self.list_to_str(up)]
        )

        result = o_feed.order_by('-created')[offset:(limit + offset)]

        if count:
            return result, o_feed.count()

        return result


    class Meta:
        db_table = 'users_feed'
        app_label = 'users'
        verbose_name = u'Лента событий'
        verbose_name_plural = u'Ленты событий'
