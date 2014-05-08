# coding: utf-8
from django.core.management.base import BaseCommand
from django.core.files import File

from apps.contents.models import Locations
from apps.films.constants import APP_FILM_TYPE_ADDITIONAL_MATERIAL_POSTER

from crawler.nichego_poster import get_poster

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


class Command(BaseCommand):

    
    def handle(self, *args, **kwargs):
        j = 0
        i = -1
        for i,location in enumerate(Locations.objects.all()):
            try:
                val = URLValidator()
                # Validating that given url_view exists
                val(location.url_view)
            except ValidationError , ve:
                location.delete()
                j += 1

        print "%d of %d locations deleted" %(j,i+1)

