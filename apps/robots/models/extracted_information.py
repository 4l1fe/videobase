from django.db import models

class ExtractedInformation(models.Model):

    domain = models.ForeignKey('ExternalSources' , verbose_name = u'External Source')
    film   = models.ForeignKey(Films, verbose_name = u'Фильм')
    rtry   = models.ForeignKey(RobotTries,verbose_name = 'Try')
    price  = models.IntegerField(verbose_name = 'Price')
    url    = models.URLField(max_length = 255,verbose_name='URL to film information')



    def __unicode__(self):
        return u'[{0}] {1}'.format(self.pk, self.domain)

    class Meta:
        # Имя таблицы в БД
        db_table = 'robots_extsources'
        app_label = 'robots'
        verbose_name = u'Внешние источники'
        verbose_name_plural = u'Внешние источники'
