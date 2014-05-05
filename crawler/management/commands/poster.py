# coding: utf-8
from django.core.management.base import BaseCommand
from django.core.files import File

from apps.films.models import Films, FilmExtras
from apps.films.constants import APP_FILM_TYPE_ADDITIONAL_MATERIAL_POSTER

from crawler.nichego_poster import get_poster


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        films = Films.objects.all()
        for film in films:
            poster = get_poster(film)
            if poster:
                print u"Adding poster for {}".format(film)
                fe = FilmExtras(film=film, type=APP_FILM_TYPE_ADDITIONAL_MATERIAL_POSTER,
                                name=u"Постер для {}".format(film.name),
                                name_orig=u"Poster for {}".format(film.name),
                                description=" ")
                fe.save()
                print u"Created film extras {}".format(fe.pk)
                fe.photo.save('poster.jpg', File(poster))

