# coding: utf-8

from django.core.management.base import BaseCommand, CommandError
from apps.films.models import Films, PersonsFilms, Persons, Genres, FilmExtras, Countries
from apps.films.constants import APP_PERSON_PHOTO_DIR,APP_FILM_CRAWLER_LIMIT,APP_FILM_CRAWLER_DELAY,APP_FILM_TYPE_ADDITIONAL_MATERIAL_POSTER, APP_FILM_FULL_FILM
from apps.robots.models import KinopoiskTries
from apps.robots.constants import APP_ROBOT_FAIL, APP_ROBOT_SUCCESS
from crawler.parse_page import acquire_page, parse_one_page
from django.core.files import File
from optparse import make_option
from crawler.kinopoisk_poster import set_kinopoisk_poster
from time import sleep
from django.utils.timezone import now
import logging
from crawler.kinopoisk import parse_from_kinopoisk
    
    
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
        page_dump = u"Couldn't get page"

        logger.info("Starting crawler")

        if args:
            films = [Films.objects.get(pk=arg) for arg in args]
        else:
            films = Films.objects.filter(kinopoisk_lastupdate=None, kinopoisk_id__isnull=False)[:LIMIT]

        for film in films:
            previous_tries = KinopoiskTries.objects.filter(result=APP_ROBOT_FAIL, film=film)
            if film.kinopoisk_id and ((not previous_tries) or options['debug']):
                sleep(APP_FILM_CRAWLER_DELAY)
                parse_from_kinopoisk(film,film.kinopoisk_id)

