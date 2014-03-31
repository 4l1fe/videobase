# coding: utf-8
import requests
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
        self.params = {'q': self.film.name, 'json': 1, 'limit': 1}

    # Поиск фильма
    def __search(self, load_function):
        url = "http://%s/%s" % (self.host, self.search_url, )
        response = load_function(url, params=self.params)
        film = parsers.parse_search(response)
        if film is None:
            raise Exception()
        self.url_load = film['link']

    # Загрузка самой страници с фильмом
    def load(self, load_function=requests.get):
        self.__search(load_function)
        url = "http://%s%s" % (self.host, self.url_load)
        html = load_function(url, params=self.params)
        if html is None:
            raise Exception()