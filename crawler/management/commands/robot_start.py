# coding: utf-8
""" Command to crawler sites"""

from django.core.management.base import BaseCommand
from optparse import make_option

from apps.films.models import Films, Seasons
from apps.contents.models import Contents, Locations
from apps.films.constants import APP_FILM_CRAWLER_LIMIT
from crawler.ivi_ru.loader import IVI_Loader
from crawler.ivi_ru.parsers import ParseFilmPage
from crawler.core.browser import RetrievePageException
from requests.exceptions import ConnectionError
from apps.robots.constants import APP_ROBOTS_TRY_SITE_UNAVAILABLE,APP_ROBOTS_TRY_NO_SUCH_PAGE, APP_ROBOTS_TRY_PARSE_ERROR, APP_ROBOTS_TRY_SUCCESS 
from apps.robots.models import RobotsTries
import logging
import re
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


def sane_dict(film):
    return {'name': film.name,
            'name_orig': film.name_orig,
            'number': None,
            'description': film.description,
            'release_date': film.release_date,
            'series_cnt': None,
            'viewer_cnt': 0,
            'viewer_lastweek_cnt': 0,
            'viewer_lastmonth_cnt': 0
    }
            

def get_content(film, **kwargs):

    # Getting all content with this film
    contents = Contents.objects.filter(film=film)

    if 'season_num' in kwargs:
        season_num = kwargs['season_num']
    else:
        season_num = None

    if 'release_date' in kwargs:
        release_date = kwargs['release_date']
    else:
        release_date = None

    if 'description' in kwargs:
        description = kwargs['description']
    else:
        description = None

    if len(contents) == 0:
        #If there is no such content just creating one with meaningfull defaults

        if not season_num is None:
            raise NameError("Variant with new TV series not in db not implemented")
        content = Contents(film=film, name=film.name, name_orig=film.name_orig, description=description,
                           release_date=film.release_date, viever_cnt=0, viever_lastweek_cnt=0)
        content.save()
        
    else:
        if season_num is None:
            content = contents[0]
        else:
            content = next((c for c in contents if c.season.number == season_num), None)

            if content is None:

                precontent = contents[0]
                if release_date is None:
                    logging.debug("Assigned release date for new content based on release date for the film %d", film.pk)
                    release_date = film.release_date

                if 'series_cnt' in kwargs:
                    series_cnt = kwargs['series_cnt']
                else:
                    logging.debug("Assigned new series count in season to number of series in previous season for season %d for film %d", season_num, film.pk)
                    series_cnt = precontent.season.series_cnt
                    
                season = Seasons(film=film, release_date=release_date, series_cnt=series_cnt,
                                 description=description, number=season_num)
                content = Contents(film=film, name=precontent.name, name_orig=precontent.name_orig,
                                   description=description, number=season_num, release_date=release_date, viewer_cnt=0,
                                   season=season, viewer_lastweek_cnt=0, viewer_lastmonth_cnt=0)

                content.save()

        return content


def save_location(film, **kwargs):
    content = get_content(film, **kwargs)
    location = Locations(content=content, **kwargs)
    location.save()


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
                
        except ConnectionError, ce:
            # Couldn't conect to server
            m = re.match(".+host[=][']([^']+)['].+", ce.message.message)

            host = m.groups()[0]
            url = ce.message.url

            robot_try = RobotsTries(domain = host,
                                   url = 'http://'+host+url,
                                   film = film,
                                   outcome = APP_ROBOTS_TRY_SITE_UNAVAILABLE
            )

            robot_try.save()
            
        except RetrievePageException, rexp:
            # Server responded but not 200

            robot_try = RobotsTries(domain = site,
                                   url = rexp.url,
                                   film = film,
                                   outcome = APP_ROBOTS_TRY_NO_SUCH_PAGE
            )

            robot_try.save()
        except:
            # Most likely parsing error
            robot_try = RobotsTries(domain = site,
                                   url=rexp.url,
                                   film=film,
                                   outcome=APP_ROBOTS_TRY_PARSE_ERROR
            )

            robot_try.save()

            