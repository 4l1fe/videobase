# coding: utf-8
""" Command to crawler sites"""

from django.core.management.base import BaseCommand
from optparse import make_option

from apps.films.models.films import Films
from apps.films.constants import APP_FILM_CRAWLER_LIMIT
from crawler.ivi_ru.loader import IVI_Loader
from crawler.ivi_ru.parsers import ParseFilmPage

from crawler import Robot

# Список допустимых сайтов
sites = ('ivi.ru', 'zoomby.ru', 'now.ru', 'playfamily.ru', 'amediateka.ru')

# Словарь сайтов:
# louder: загрузчик страници
# parser: парсер страници фильма
sites_crawler = {
    'ivi.ru': {'loader': IVI_Loader,
               'parser': ParseFilmPage},
    'zoomby.ru': {'loader': None,
                  'parser': None},
    'megogo.net': {'loader': None,
                   'parser': None},
    'now.ru': {'loader': None,
               'parser': None},
    'playfamily.ru': {'loader': None,
                      'parser': None},
    'amediateka.ru': {'loader': None,
                      'parser': None},
}


class Command(BaseCommand):
    help = u'Запустить краулеры'
    requires_model_validation = True
    option_list = BaseCommand.option_list + (
        make_option('--limit',
                    dest='limit',
                    default=APP_FILM_CRAWLER_LIMIT,
                    help=u'How much films to process'),
        make_option('--site',
                    type='choice',
                    choices=sites,
                    dest='site',
                    action='store',
                    help=u'Site for crawling'),
    )

    def handle(self, *args, **options):
        film = Films.objects.filter(pk=1)
        site = options['site']
        try:
            robot = Robot(films=film, **sites_crawler[site])
            for data in robot.get_data():
                pass
        except Exception:
            pass