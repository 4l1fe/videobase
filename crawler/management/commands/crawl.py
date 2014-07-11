# coding: utf-8

from django.core.management.base import BaseCommand
from apps.films.models import Films
from apps.films.constants import APP_FILM_CRAWLER_LIMIT, APP_FILM_CRAWLER_DELAY
from apps.robots.models import KinopoiskTries
from apps.robots.constants import APP_ROBOT_FAIL
from optparse import make_option
from time import sleep
from crawler.kinopoisk_ru.kinopoisk import parse_from_kinopoisk
    
    
class Command(BaseCommand):

    help = u'Запустить краулер'
    requires_model_validation = True
    option_list = BaseCommand.option_list + (
        make_option('--limit',
                    dest='limit',
                    default=APP_FILM_CRAWLER_LIMIT,
                    help=u'How much films to process'),
        make_option('--debug',
                    dest='debug',
                    action='store_true',
                    default=False,
                    help=u'Repeat films crawling for which has failed'),
    )

    def handle(self, *args, **options):
        if args:
            films = [Films.objects.get(pk=arg) for arg in args]
        else:
            films = Films.objects.filter(kinopoisk_lastupdate=None, kinopoisk_id__isnull=False)

        for film in films:
            previous_tries = KinopoiskTries.objects.filter(result=APP_ROBOT_FAIL,film=film)
            if film.kinopoisk_id and ((not previous_tries) or options['debug']):
                sleep(APP_FILM_CRAWLER_DELAY)
                parse_from_kinopoisk(film, film.kinopoisk_id)

