from django.db import models


class Legal(models.Model):
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'Legal {:%d-%m-%Y}'.format(self.updated)

    class Meta:
        db_table = 'legal'
        app_label = 'contents'
