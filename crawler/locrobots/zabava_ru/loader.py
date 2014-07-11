# coding: utf-8
HOST = 'www.zabava.ru'
URL_SEARCH = 'search'
URL_LOAD = ''
from crawler.core.exceptions import NoSuchFilm
import parsers
from crawler.core import BaseLoader


class ZABAVAR_RU_Loader(BaseLoader):
    def __init__(self,  film, host=HOST, url_load=URL_LOAD):
        super(ZABAVAR_RU_Loader, self).__init__(film, host, url_load)
        self.search_url = URL_SEARCH
        self.params = {'searchField':  self.film.name}

    def get_url(self, load_function):
        url = "http://%s/%s" % (self.host, self.search_url, )
        response = load_function(url, params=self.params, cache=False)
        film_url = parsers.parse_search(response, self.film.name)
        if film_url is None:
            raise NoSuchFilm(self.film)
        self.url_load = film_url
        return self.url_load
