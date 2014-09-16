# coding: utf-8

from django.db import models

from utils.fields.currency_field import CurrencyField
from apps.contents.constants import APP_CONTENTS_LOC_TYPE, APP_CONTENTS_PRICE_TYPE


#############################################################################################################
# Модель Месторасположения контента
class Locations(models.Model):
    content    = models.ForeignKey('Contents', verbose_name=u'Контент', related_name='location')
    type       = models.CharField(choices=APP_CONTENTS_LOC_TYPE, db_index=True, verbose_name=u'Тип', max_length=40)
    lang       = models.CharField(max_length=40, verbose_name=u'Язык')
    quality    = models.CharField(max_length=40, verbose_name=u'Качество')
    subtitles  = models.CharField(max_length=40, verbose_name=u'Субтитры')
    price      = CurrencyField(db_index=True, verbose_name=u'Цена')
    price_type = models.SmallIntegerField(choices=APP_CONTENTS_PRICE_TYPE, db_index=True, verbose_name=u'Тип цены')
    url_view   = models.URLField(max_length=255, verbose_name=u'Ссылка для просмотра')
    value      = models.TextField(verbose_name=u"Код встраивания", blank=True, null=True)
    created    = models.DateTimeField(auto_now_add=True, verbose_name=u'Создан')

    def as_vbLocation(self):

        return {'id': self.pk,
                'type': str(self.type),
                'lang': self.lang,
                'quality': self.quality,
                'subtitles': self.subtitles,
                'price': self.price,
                'price_type': str(self.type),
                'value': self.value
        }

    @classmethod
    def exist_location(self, pk):
        from django.db import connection
        cursor = connection.cursor()

        try:
            query = """
                SELECT * FROM "locations" LEFT JOIN "content" ON ("locations"."content_id" = "content"."id")
                WHERE "content"."film_id" = %s
            """

            cursor.execute(query, [pk])
            result = cursor.fetchone()

            if result:
                return True

        except Exception, e:
            return e
        finally:
            cursor.close()

        return False

    def __unicode__(self):
        return u'[{0}] {1} {2}'.format(self.pk, self.content.name, self.type)

    class Meta:
        # Имя таблицы в БД
        db_table = 'locations'
        app_label = 'contents'
        verbose_name = u'Месторасположения контента'
        verbose_name_plural = u'Месторасположения контента'
