# coding: utf-8
from apps.films.constants import APP_FILM_SERIAL
from crawler.core.exceptions import NoSuchFilm
from crawler.locrobots.zoomby_ru.parsers import ParseFilm
from crawler.core import BaseLoader
import urllib

HOST = 'www.zoomby.ru'
URL_LOAD = ''


class ZOOMBY_Loader(BaseLoader):
    def __init__(self, film, host=HOST, url_load=URL_LOAD):
        super(ZOOMBY_Loader, self).__init__(film, host, url_load)
        self.search_url = 'search?{}'.format(urllib.urlencode({'type':'','q': self.film}))

    def get_url(self, load_function):
        serial = False
        if self.film.type == APP_FILM_SERIAL:
            serial = True

        filmLink = ParseFilm.parse_search(self.film.name, self.film.release_date.year, load_function, serial)

        if filmLink is None:
            raise NoSuchFilm(self.film)
        self.url_load = filmLink
        return filmLink
