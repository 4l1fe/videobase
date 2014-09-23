# coding: utf-8

from django.core.management.base import BaseCommand
from apps.films.models.films import Films


class Command(BaseCommand):

    __dirt_words = (u'(ТВ)', u'(видео)')

    def handle(self, *args, **kwargs):
        self.fix_names()

    def fix_names(self, *args, **kwargs):
        films = Films.objects.all()
        for film in films:
            for word in self.__dirt_words:
                if word in film.name:
                    film.name = film.name.replace(word, '').strip()
                    film.save()