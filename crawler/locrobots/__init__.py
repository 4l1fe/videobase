# coding: utf-8
from apps.films.models import Films

from crawler.locrobots.ivi_ru.loader import IVI_Loader
from crawler.locrobots.ivi_ru.parsers import ParseFilmPage
from crawler.locrobots.now_ru.loader import NOW_Loader
from crawler.locrobots.now_ru.parsers import ParseNowFilmPage
from crawler.locrobots.megogo_net.loader import MEGOGO_Loader
from crawler.locrobots.megogo_net.parsers import ParseMegogoFilm
from crawler.locrobots.stream_ru.loader import STREAM_RU_Loader
from crawler.locrobots.stream_ru.parsers import ParseStreamFilm
from crawler.locrobots.play_google_com.loader import PLAY_GOOGLE_Loader
from crawler.locrobots.play_google_com.parsers import ParsePlayGoogleFilm
from crawler.locrobots.tvigle_ru.loader import TVIGLE_Loader
from crawler.locrobots.tvigle_ru.parsers import ParseTvigleFilm
from crawler.locrobots.videomax_org.loader import VIDEOMAX_Loader
from crawler.locrobots.videomax_org.parsers import ParseVIDEOMAXPage
from crawler.locrobots.zabava_ru.loader import ZABAVAR_RU_Loader
from crawler.locrobots.zabava_ru.parsers import ParseZabavaFilm
from crawler.locrobots.oll_tv.loader import Oll_Loader
from crawler.locrobots.oll_tv.parser import ParseOllFilm
from crawler.locrobots.tvzavr_ru.loader import Tvzavr_Loader
from crawler.locrobots.tvzavr_ru.parsers import ParseTvzavrFilmPage
from crawler.locrobots.zoomby_ru.loader import ZOOMBY_Loader
from crawler.locrobots.zoomby_ru.parsers import ParseFilm
from crawler.utils.locations_utils import save_location, sane_dict

# Словарь сайтов:
# loader: загрузчик страници
# parser: парсер страници фильма
sites_crawler = {
    'ivi_ru': {
        'loader': IVI_Loader,
        'parser': ParseFilmPage
    },
    'zoomby_ru': {
        'loader': ZOOMBY_Loader,
        'parser': ParseFilm()
    },
    'megogo_net': {
        'loader': MEGOGO_Loader,
        'parser': ParseMegogoFilm
    },
    'now_ru': {
        'loader': NOW_Loader,
        'parser': ParseNowFilmPage
    },
    'tvigle_ru': {
        'loader': TVIGLE_Loader,
        'parser': ParseTvigleFilm()
    },
    #'tvzavr_ru': {
    #     'loader': Tvzavr_Loader,
    #     'parser': ParseTvzavrFilmPage()
    # },
    'stream_ru': {
        'loader': STREAM_RU_Loader,
        'parser': ParseStreamFilm
    },
    'play_google_com': {
        'loader': PLAY_GOOGLE_Loader,
        'parser': ParsePlayGoogleFilm
    },
    'oll_tv': {
        'loader': Oll_Loader,
        'parser': ParseOllFilm()
    },
    'zabava_ru': {
        'loader': ZABAVAR_RU_Loader,
        'parser': ParseZabavaFilm
    },
    'videomax_org': {
        'loader': VIDEOMAX_Loader,
        'parser': ParseVIDEOMAXPage,
    }
}

sites = sites_crawler.keys()


def process_film_on_site(site, film_id):
    try:
        film = Films.objects.get(id=film_id)
    except Films.DoesNotExist:
        print "There is no film in db with such id"
        return None

    loaded_data = sites_crawler[site]['loader'](film).load()

    for data in sites_crawler[site]['parser'].parse(loaded_data['html'], sane_dict, film, url=loaded_data['url']):
        print u"Trying to put data from %s for %s to db" % (site, unicode(data['film']))
        save_location(**data)