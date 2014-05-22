# coding: utf-8

from django.contrib.auth.models import User
from django.db import models

from apps.users.constants import APP_FEED_TYPE, APP_USERS_API_DEFAULT_PER_PAGE
import jsonfield


class Feed(models.Model):
    """
    Содержит имена полей, которые переопределяют питоновские стандартные объекты.
    """

    user = models.ForeignKey(User, verbose_name="Пользователь", null=True, blank=True)
    created = models.DateTimeField(verbose_name="Дата создания", auto_now=True)
    type = models.CharField(verbose_name="Тип связанного объекта", choices=APP_FEED_TYPE, max_length=255, name='type')
    object = models.TextField(verbose_name="Связанный объект", name='object')
    text = jsonfield.JSONField(verbose_name="Текст", null=True, blank=True)


    def __unicode__(self):
        return u"[{id}]{type}".format(id=self.pk, type=self.get_type_display())


    @classmethod
    def get_feeds_by_user(self, user_id, uf=[], up=[], offset=0, limit=APP_USERS_API_DEFAULT_PER_PAGE, *args, **kwargs):
        sql = """
          SELECT * FROM "users_feed"
          WHERE ("users_feed"."user_id"=%s OR "users_feed"."user_id" IS NULL) AND (
            CASE "users_feed"."user_id" IS NULL WHEN
              CASE
                WHEN "users_feed"."type"=%s THEN
                  CAST(coalesce(object->>'id', '0') AS integer) IN %s
                WHEN "users_feed"."type"=%s THEN
                  CAST(coalesce(object->>'id', '0') AS integer) IN %s
                ELSE true END
              ELSE true
            END)
          ORDER BY "users_feed"."created" DESC OFFSET %s LIMIT %s;
        """
        params = [user_id,  'film_o', tuple(uf), 'pers_o', tuple(up), offset, limit]

        return self.objects.raw(sql, params)

    class Meta:
        db_table = 'users_feed'
        app_label = 'users'
        verbose_name = u'Лента событий'
        verbose_name_plural = u'Ленты событий'