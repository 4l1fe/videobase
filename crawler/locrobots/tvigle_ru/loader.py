# coding: utf-8
from apps.films.constants import APP_FILM_SERIAL
from crawler.core.exceptions import NoSuchFilm
from parsers import ParseTvigleFilm
from crawler.core import BaseLoader
import urllib

HOST = 'www.tvigle.ru'
URL_LOAD = ''


class TVIGLE_Loader(BaseLoader):
    def __init__(self, film, host=HOST, url_load=URL_LOAD):
        super(TVIGLE_Loader, self).__init__(film, host, url_load)
        search_film = self.film.name.strip().replace(' ', '+')
        self.search_url = 'search/?q=' + search_film

    def get_url(self, load_function):
        if self.film.type == APP_FILM_SERIAL:
            url = "http://%s/%s" % (self.host, "catalog/filmy-i-serialy/serialy/")
        else:
            url = 'http://www.tvigle.ru/catalog/filmy-i-serialy/filmy/'
        return url
