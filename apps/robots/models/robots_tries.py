# coding: utf-8

from django.db import models

from apps.films.models import Films
from apps.robots.models import ExternalSources
from ..constants import APP_ROBOTS_TRY_OUTCOME


#############################################################################################################
# Модель Попытки получить информацию о фильме с сайта
class RobotsTries(models.Model):
    '''
    Log of robot attempt to get information from particular domain
    for particular film
    '''

    domain = models.CharField(max_length=255, verbose_name = u'Домен'
    try_time = models.DateTimeField(auto_now_add=True,
                                    editable=False,
                                    verbose_name=u'Дата попытки')
    film = models.ForeignKey(Films, verbose_name=u'Фильм')
    url = models.URLField(max_length=255,
                             verbose_name=u'URL to film information')
    outcome = models.CharField(max_length=255,
                               choices=APP_ROBOTS_TRY_OUTCOME,
                               verbose_name=u'Результат')

    def __unicode__(self):
        return u'[{0}] {1}'.format(self.pk, self.domain)

    class Meta:
        # Имя таблицы в БД
        db_table = 'robots_tries'
        app_label = 'robots'
        verbose_name = u'Результат попытки'
        verbose_name_plural = u'Результаты попыток'

