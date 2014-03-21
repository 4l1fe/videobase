# coding: utf-8

from django.core.management.base import NoArgsCommand, CommandError
from apps.films.models import Films,PersonsFilms,Persons

from crawler.imdbratings import ny_full_dict
from itertools import chain
import datetime
import HTMLParser
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


class Command(NoArgsCommand):

    help = u'Обновить IMDB рейтинг'
    requires_model_validation = True

    def handle_noargs(self, **options):

        h = HTMLParser.HTMLParser()
        full_dict = ny_full_dict(True)
        name_dict =dict((key[1],value) for key,value in full_dict.items())

        for i,film in enumerate(Films.objects.all()):
            key = h.unescape(film.name_orig).lower().strip()
            if len(film.name_orig) < 3:
                continue

            if key in name_dict:
                logger.info((u"Found rating for {} ".format(film.name_orig)).encode("utf-8"))
                rdict = name_dict[key]
                logger.debug(("Rating before {} Count before {} ".format(film.rating_imdb,film.rating_imdb_cnt)).encode("utf-8"))
                film.rating_imdb=rdict['rating']
                film.rating_imdb_cnt=rdict['votes']
                logging.debug(("Rating after {} Count after {}".format(film.rating_imdb,film.rating_imdb_cnt)).encode("utf-8"))
                film.save()

