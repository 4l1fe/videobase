# coding: utf-8
""" Module containing general functionality for crawler robots
and run function for robots written as loader parser combo
"""

from django.utils import timezone
from django.db.models import Q
from apps.films.models import Films
from django.core.exceptions import ValidationError
from crawler.locations_utils import save_location,sane_dict





from crawler.kinopoisk import get_id_by_film
from crawler.ivi_ru.loader import IVI_Loader
from crawler.ivi_ru.parsers import ParseFilmPage
from crawler.now_ru.loader import NOW_Loader
from crawler.now_ru.parsers import ParseNowFilmPage
from crawler.megogo_net.loader import MEGOGO_Loader
from crawler.megogo_net.parsers import ParseMegogoFilm
from crawler.stream_ru.loader import STREAM_RU_Loader
from crawler.stream_ru.parsers import ParseStreamFilm
from crawler.core.exceptions import NoSuchFilm, RetrievePageException
from crawler.play_google_com.loader import PLAY_GOOGLE_Loader
from crawler.play_google_com.parsers import ParsePlayGoogleFilm
from crawler.playfamily_dot_ru.loader import playfamily_loader
from crawler.playfamily_dot_ru.parser import PlayfamilyParser
from crawler.tvigle_ru.loader import TVIGLE_Loader
from crawler.tvigle_ru.parsers import ParseTvigleFilm
from crawler.zabava_ru.loader import ZABAVAR_RU_Loader
from crawler.zabava_ru.parsers import ParseZabavaFilm
from crawler.oll_tv.loader import Oll_Loader
from crawler.oll_tv.parser import ParseOllFilm
from crawler.tvzavr_ru.loader import Tvzavr_Loader
from crawler.tvzavr_ru.parsers import ParseTvzavrFilmPage
from crawler.zoomby_ru.loader import ZOOMBY_Loader
from crawler.zoomby_ru.parsers import ParseFilm



from requests.exceptions import ConnectionError
from apps.robots.constants import APP_ROBOTS_TRY_SITE_UNAVAILABLE, APP_ROBOTS_TRY_NO_SUCH_PAGE, \
    APP_ROBOTS_TRY_PARSE_ERROR
from apps.robots.models import RobotsTries, Robots

import re
from crawler import Robot
import json


# Словарь сайтов:
# loader: загрузчик страници
# parser: парсер страници фильма
sites_crawler = {
    'ivi_ru': {'loader': IVI_Loader,
               'parser': ParseFilmPage},
    'zoomby_ru': {'loader': ZOOMBY_Loader,
                  'parser': ParseFilm()},
    'megogo_net': {'loader': MEGOGO_Loader,
                   'parser': ParseMegogoFilm},
    'now_ru': {'loader': NOW_Loader,
               'parser': ParseNowFilmPage},
    'tvigle_ru': {'loader': TVIGLE_Loader,
                  'parser': ParseTvigleFilm()},
    #'tvzavr_ru': {'loader': Tvzavr_Loader,
    #            'parser': ParseTvzavrFilmPage()},
    'stream_ru': {'loader': STREAM_RU_Loader,
                  'parser': ParseStreamFilm},
    'play_google_com': {'loader': PLAY_GOOGLE_Loader,
                        'parser': ParsePlayGoogleFilm},
    'oll_tv': {'loader': Oll_Loader,
               'parser': ParseOllFilm()},
    'zabava_ru': {'loader': ZABAVAR_RU_Loader,
                  'parser': ParseZabavaFilm}
}
sites = sites_crawler.keys()


def robot_exceptions(func):
    def wrapper(*args,**kwargs):

        if 'site' in kwargs:
            site = kwargs['site']
        else:
            site = args[1]
        try:

            func(*args,**kwargs)
        except ConnectionError, ce:
            # Couldn't conect to server
            print u"Connection error"
            m = re.match(".+host[=][']([^']+)['].+", ce.message.message)

            host = m.groups()[0]
            url = ce.message.url
            if host is None:
                host = 'unknown'

            robot_try = RobotsTries(domain=host,
                                url='http://' + host + url,
                                film=args[0][0],
                                outcome=APP_ROBOTS_TRY_SITE_UNAVAILABLE
                                )

            robot_try.save()

        except RetrievePageException, rexp:
            # Server responded but not 200
            print u"RetrievePageException"
            if site is None:
                site = 'unknown'

                robot_try = RobotsTries(domain=site,
                                url=rexp.url,
                                film=args[0][0],
                                outcome=APP_ROBOTS_TRY_NO_SUCH_PAGE
                                )

                robot_try.save()

        except UnicodeDecodeError:
            print "Unicode error"
            if site is None:
                site = 'unknown'

                robot_try = RobotsTries(domain=site,
                                film=args[0][0],
                                outcome=APP_ROBOTS_TRY_PARSE_ERROR
                                )

            robot_try.save()

        except ValidationError as ve:

            print "Tried to save location with invalid URL"

        except NoSuchFilm as e:
            robot_try = RobotsTries(domain=site,
                                    film=e.film,
                                    outcome=APP_ROBOTS_TRY_NO_SUCH_PAGE)
            
            robot_try.save()
        except Exception,e:
            print "Unknown exception {}".format(e)
            
    return wrapper
    

@robot_exceptions    
def process_film_on_site(site,film_id):

    try:
        film = [Films.objects.get(id=film_id),]
    except Films.DoesNotExist:
        print "There is no film in db with such id"
        return
    robot = Robot(films=film, **sites_crawler[site])
    for data in robot.get_data(sane_dict):
        print u"Trying to put data from %s for %s to db" % (site, unicode(data['film']))
        save_location(**data)


def launch_next_robot_try_for_kinopoisk(robot):
    robot.last_start = timezone.now()
    robot.save()

    films = Films.objects.filter(~Q(robots_tries__outcome=APP_ROBOTS_TRY_NO_SUCH_PAGE),
                                 kinopoisk_id__isnull=True)[:10]
    for film in films:
        try:
            id = get_id_by_film(film)
            film.kinopoisk_id = id
            film.save()
        except RetrievePageException as rexp:
            # Server responded but not 200
            print u"RetrievePageException"
            robot_try = RobotsTries(domain='kinopoisk_ru',
                                    url=rexp.url,
                                    film=film[0],
                                    outcome=APP_ROBOTS_TRY_NO_SUCH_PAGE)

            robot_try.save()
        except UnicodeDecodeError:
            print "Unicode error"
            robot_try = RobotsTries(domain='kinopoisk_ru',
                                    film=film, outcome=APP_ROBOTS_TRY_PARSE_ERROR)

            robot_try.save()
        except Exception as e:
            print "Unknown exception %s", str(e)
            robot_try = RobotsTries(domain='kinopoisk_ru', film=film,
                                    outcome=APP_ROBOTS_TRY_PARSE_ERROR)
            robot_try.save()

