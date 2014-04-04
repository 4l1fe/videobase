# coding: utf-8
from crawler.core.exseptions import NoSuchFilm

import parsers
from ..core import BaseLoader


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
        self.params = {'q': self.film.name + ' ', 'json': 1, 'limit': 1}

    # Поиск фильма
    def get_url(self, load_function):
        url = "http://%s/%s" % (self.host, self.search_url, )
        response = load_function(url, params=self.params, cache=False)
        film = parsers.parse_search(response)
        if film is None:
            raise NoSuchFilm(self.film)
        self.url_load = film['link']
        return "http://%s%s" % (self.host, self.url_load)
