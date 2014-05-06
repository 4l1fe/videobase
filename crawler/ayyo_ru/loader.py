# coding: utf-8
import requests
import urllib
HOST = 'www.ayyo.ru'
URL_SEARCH = 'api/search/live/?{}'
URL_LOAD = ''
from crawler.core.exceptions import NoSuchFilm
import parsers
from ..core import BaseLoader


class AYYO_RU_Loader(BaseLoader):
    def __init__(self,  film, host=HOST, url_load=URL_LOAD):
        super(AYYO_RU_Loader, self).__init__(film, host, url_load)
        self.search_film = urllib.urlencode({'text': (self.film.name.encode('utf-8'))})
        self.search_url = URL_SEARCH.format(self.search_film)

    def get_url(self, load_function):
        url = "https://%s/%s" % (self.host, self.search_url, )
        response = requests.get(url, headers={"Accept": "application/vnd.ayyo.api+json; version=1.2", "Authorization": "Bearer 1db6377876"})
        film_url = parsers.parse_search(response, self.film.name)
        if film_url is None:
            raise NoSuchFilm(self.film)
        self.url_load = film_url
        return self.url_load
