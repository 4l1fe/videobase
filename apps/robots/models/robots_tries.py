# coding: utf-8
from django.db import models

from apps.films.models import Films
from ..constants import APP_ROBOTS_TRY_OUTCOME


#############################################################################################################
# Модель Попытки получить информацию о фильме с сайта
class RobotsTries(models.Model):
    '''
    Log of robot attempt to get information from particular domain
    for particular film
    '''

    domain = models.CharField(max_length=255, verbose_name=u'Домен')
    film = models.ForeignKey(Films, verbose_name=u'Фильм', related_name='robots_tries')
    url = models.URLField(max_length=255, verbose_name=u'URL to film information', null=True, blank=True)
    outcome = models.CharField(max_length=255, choices=APP_ROBOTS_TRY_OUTCOME, verbose_name=u'Результат')

    def __unicode__(self):
        return u'[{0}] {1}'.format(self.pk, self.domain)

    class Meta:
        # Имя таблицы в БД
        db_table = 'robots_tries'
        app_label = 'robots'
        verbose_name = u'Попытка'
        verbose_name_plural = u'Попытки'

