from django.db import models

class ExtractedInformation(models.Model):

    rtry   = models.ForeignKey('RobotTries',verbose_name = 'Try')
    price  = models.IntegerField(verbose_name = 'Price')
    mobile = models.BooleanField(verbose_name = 'Is available on mobile ?')
    smart_tv = models.BooleanField(verbose_name = 'Is available on Smart TV ?')
    computer = models.BooleanField(verbose_name = 'Is available on PC ?')
    

    def __unicode__(self):
        return u'[{0}] {1}'.format(self.pk, self.domain)

    class Meta:
        # Имя таблицы в БД

        db_table = 'robots_extracted_information'
        app_label = 'robots'
        verbose_name = u'Extracted information'
        verbose_name_plural = u'Extracted information'

