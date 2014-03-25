import os
from utils.common import get_thumbnail_url
from django.db import models
from ..constants import APP_PERSON_PHOTO_DIR


class PhotoClass(models.Model):

    class Meta:
        abstract = True

    def image_file(self):
        if self.photo:
            return self.get_thumbnail_html
        else:
            return '(none)'

    @property
    def get_thumbnail_html(self):
        html = '<a class="image-picker" href="%s"><img src="%s" alt="%s" /></a>'
        return html % (self.photo.url, get_thumbnail_url(self.photo.url), "")

    image_file.short_description = 'thumbnail'
    image_file.allow_tags = True

    def save(self, *args, **kwargs):
        is_new = self.pk == None
        super(PhotoClass, self).save(*args, **kwargs)

        if is_new:
            instance_photo = self.photo
            if instance_photo:
                # Create new filename, using primary key
                oldfile = self.photo.name
                newfile = os.path.join(APP_PERSON_PHOTO_DIR, str(self.id), oldfile.split("/")[-1])

                # Magic with photo
                self.photo.storage.delete(newfile)
                self.photo.storage.save(newfile, instance_photo)
                self.photo.name = newfile
                self.photo.close()
                self.photo.storage.delete(oldfile)

                # Save again to keep changes
                super(PhotoClass, self).save(*args, **kwargs)
