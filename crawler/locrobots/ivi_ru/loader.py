# coding: utf-8
from crawler.core.exceptions import NoSuchFilm
from crawler.tor import simple_tor_get_page
from crawler.core.loader import BaseLoader
from utils.common import url_with_querystring

import parsers

HOST = 'www.ivi.ru'
URL_SEARCH = 'search/ajax/new/autocomplete'
URL_LOAD = ''


# Загрузка страници с фильмом
class IVI_Loader(BaseLoader):
    def __init__(self, film, host=HOST, url_load=URL_LOAD):
        super(IVI_Loader, self).__init__(film, host, url_load)
        # url для поиска фильмов
        self.search_url = URL_SEARCH
        # параметры для поиска
        self.params = {'q': self.film.name + ' ', 'json': 1, 'limit': 10}

    # Поиск фильма
    def get_url(self, load_function):
        url = "http://%s/%s" % (self.host, self.search_url, )
        url = url_with_querystring(url, **self.params)
        response = load_function(url)
        film = parsers.parse_search(response, self.film)
        if film is None:
            raise NoSuchFilm(self.film)
        self.url_load = film['link']
        return "http://%s%s" % (self.host, self.url_load)