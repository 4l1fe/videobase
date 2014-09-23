# coding: utf-8
from django.db import models


################################################################################
# Модель сервиса трансляции
class CastsServices(models.Model):
    name        = models.CharField(max_length=255, unique =True, db_index=True, verbose_name=u'Название')
    url         = models.CharField(max_length=255, default='', blank=True, db_index=True, verbose_name=u'Ссылка')
    description = models.TextField(max_length=255, db_index=True, blank=False, verbose_name=u'Описание')
    update      = models.DateTimeField(null=True, blank=True, verbose_name=u'Время обновления')
    tags        = models.ManyToManyField('AbstractCastsTags', verbose_name=u'Теги', related_name='casts_services')

    def __unicode__(self):
        return u'[{0}] {1} - {2}'.format(self.pk, self.name, self.url)

    class Meta:
        # Имя таблицы в БД
        db_table = 'casts_services'
        app_label = 'casts'
        verbose_name = u'Сервис трансляций'
        verbose_name_plural = u'Сервисы трансляций'
