# coding: utf-8

from ..core.browser import simple_get
from crawler.core.exceptions import RetrievePageException

# Базовый класс загрузчика страници
class BaseLoader(object):
    """ Base class to load html from site"""
    def __init__(self, film, host, url_load, params=None):
        # Хост откуда скачиваем
        self.host = host
        # Наш фильм который ищим
        self.film = film
        # url для взятие фильма( шаблон)
        self.url_load = url_load
        self.params = {} if params is None else params

    # получить url для загрузки страници с фильмом
    def get_url(self, load_function):
        raise NotImplementedError()

    # сама функция загрузки
    def load(self, load_function=simple_get):
        try:
            url = self.get_url(load_function)
            return {'html': load_function(url), 'url': url}
        except RetrievePageException as e:
            raise RetrievePageException(url=e.url, status_code=e.status_code, film=self.film)

