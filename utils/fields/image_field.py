# coding: utf-8

import os, re

from django.db.models import ImageField
from django.db.models.signals import post_save, post_init

from django.dispatch import dispatcher


#############################################################################################################
# Собственное поле для изображения
class CustomImageField(ImageField):

    def contribute_to_class(self, cls, name):
        """Hook up events so we can access the instance."""
        super(CustomImageField, self).contribute_to_class(cls, name)
        post_init.connect(self._move_image, sender=cls)

    def _move_image(self, instance=None, **kwargs):
        if hasattr(instance, 'get_upload_to'):
            src = getattr(instance, self.attname)
            if src:
                m = re.match(r"%s/(.*)" % self.upload_to, src)
                if m:
                    pass
                #     if self.use_key:
                #         dst = "%s/%d_%s" % (instance.get_upload_to(self.attname), instance.id, m.groups()[0])
                #     else:
                #         dst = "%s/%s" % (instance.get_upload_to(self.attname), m.groups()[0])

                    # basedir = "%s%s/" % (settings.MEDIA_ROOT, os.path.dirname(dst))
                    # mkpath(basedir)

                    # shutil.move("%s%s" % (settings.MEDIA_ROOT, src),"%s%s" % (settings.MEDIA_ROOT, dst))
                    # setattr(instance, self.attname, dst)
                    # instance.save()

    def db_type(self):
        """Required by Django for ORM."""
        return 'varchar(1000)'
