# coding: utf-8

from django.core.management.base import BaseCommand, CommandError
from apps.films.models import Films, PersonsFilms, Persons, Genres, FilmExtras, Countries
from apps.films.constants import APP_PERSON_PHOTO_DIR,APP_FILM_CRAWLER_LIMIT,APP_FILM_CRAWLER_DELAY,APP_FILM_TYPE_ADDITIONAL_MATERIAL_POSTER
from apps.robots.models import KinopoiskTries
from apps.robots.constants import APP_ROBOT_FAIL, APP_ROBOT_SUCCESS
from crawler.parse_page import acquire_page, parse_one_page, get_poster
from django.core.files import File
from itertools import chain
from optparse import make_option
import datetime
import os
from time import sleep
from django.utils.timezone import now
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

LIMIT = 10


def get_person(name):

    f = Persons.objects.filter(name=name)

    if f:
        return f[0]
    else:
        p = Persons(name=name,photo='')
        p.save()
        logging.debug(u'Added Person {}'.format(name))
        return p


def get_genre(name):
    g = Genres.objects.filter(name = name)
    if g:
        return g[0]
    else:
        go = Genres(name=name,description = '')
        go.save()
        logging.debug(u'Added Genre {}'.format(name))
        return go


def get_country(name):
    g = Countries.objects.filter(name= name)
    if g:
        return g[0]
    else:
        go = Countries(name=name, description='')
        go.save()
        logging.debug(u'Added Country {}'.format(name))
        return go

flatland = get_country(u'Флатландию')


def process_film(film, pdata):
    a = []
    for d in pdata['Films']:
        a.extend(d.items())
    for key, value in dict(a).items():
        setattr(film, key, value)
    film.kinopoisk_lastupdate = now()

    film.save()
    logger.debug("Updated data for {}".format(film))

    for p in pdata['Persons']:
        po = get_person(p['name'])
        if 'photo' in p:
            if not (po.photo or (p['photo'] is None)):
                po.photo.save('profile.jpg',File(p['photo']))

        if PersonsFilms.objects.filter(film=film,person=po):
            pass
        else:
            pf = PersonsFilms(person=po, film=film, p_type=p['p_type'])
            pf.save()
    for g in pdata['Genres']:
        go = get_genre(g['name'])
        if not(go in film.genres.all()):
            film.genres.add(go)

    for c in pdata['Countries']:
        if flatland in film.countries.all():
            film.countries.remove(flatland)
        co = get_country(c['name'])
        if not(co in film.countries.all()):
            film.countries.add(co)

    poster = get_poster(film.kinopoisk_id)

    if poster:
        logging.debug("Adding poster for %s", film)
        fe = FilmExtras(film=film, type=APP_FILM_TYPE_ADDITIONAL_MATERIAL_POSTER, name=u"Постер для {}".format(film.name),
                        name_orig=u"Poster for {}".format(film.name), description=" ")
        fe.save()
        logging.debug("Created film extras %d", fe.pk)
        fe.photo.save('poster.jpg', File(poster))


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
                try:
                    page_dump = acquire_page(film.kinopoisk_id)
                    pdata = parse_one_page(page_dump)
                    process_film(film, pdata)
                    kpt = KinopoiskTries(film = film,try_time = now(),result = APP_ROBOT_SUCCESS)
                    kpt.save()
                except Exception, e:
                    logging.debug("Caught exception : %s", str(e))
                    kpt = KinopoiskTries(film = film,try_time = now(),result = APP_ROBOT_FAIL , error_message = str(e), page_dump = page_dump)
                    kpt.save()


