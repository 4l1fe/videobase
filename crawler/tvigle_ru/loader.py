# coding: utf-8
from apps.films.constants import APP_FILM_SERIAL
from crawler.core.exceptions import NoSuchFilm
import requests
import parsers
from ..core import BaseLoader
import urllib

HOST = 'www.tvigle.ru'
URL_LOAD = ''

class TVIGLE_Loader(BaseLoader):
    def __init__(self, film, host=HOST, url_load=URL_LOAD):
        super(TVIGLE_Loader, self).__init__(film, host, url_load)
        search_film = urllib.urlencode({'search_text':(self.film.name.encode('cp1251'))})
        self.search_url = 'category/search/?{}'.format(search_film)

    def get_url(self, load_function):
        serial = False
        url = "http://%s/%s" % (self.host, self.search_url, )
        response = load_function(url)
        if self.film.type == APP_FILM_SERIAL:
            serial = True
        film_link = parsers.parse_search(response, self.film.name, serial)
        if film_link is None:
            raise NoSuchFilm(self.film)
        return film_link
