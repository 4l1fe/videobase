from django.db import models


class About(models.Model):
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'About {:%d-%m-%Y}'.format(self.updated)

    class Meta:
        db_table = 'about'
        app_label = 'contents'
