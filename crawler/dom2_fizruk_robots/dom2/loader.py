# coding: utf-8
from crawler.core import BaseLoader
from crawler.core.exceptions import NoSuchFilm
from utils.common import url_with_querystring

__author__ = 'vladimir'

HOST = 'www.videomax.org'
URL_SEARCH = 'search/'
URL_LOAD = ''


# Загрузка страници с фильмом
class VIDEOMAX_Loader(BaseLoader):
    def __init__(self, film, host=HOST, url_load=URL_LOAD):
        super(VIDEOMAX_Loader, self).__init__(film, host, url_load)
        # url для поиска фильмов
        self.search_url = URL_SEARCH
        # параметры для поиска
        self.params = {'q': self.film.name}

    # Поиск фильма
    def get_url(self, load_function):
        url = "http://%s/%s" % (self.host, self.search_url, )
        url = url_with_querystring(url, **self.params)
        response = load_function(url)
        film_link = parsers.parse_search(response, self.film)
        if film_link is None:
            raise NoSuchFilm(self.film)
        self.url_load = film_link
        return film_link

