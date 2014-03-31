# coding: utf-8


# Базовый класс загрузчика страници
class BaseLoader(object):
    """ Base class to load html from site"""
    def __init__(self, film, host, url_load):
        # Хост откуда скачиваем
        self.host = host
        # Наш фильм который ищим
        self.film = film
        # url для взятие фильма( шаблон)
        self.url_load = url_load

    # сама функция загрузки
    def load(self, load_function):
        raise NotImplementedError()
