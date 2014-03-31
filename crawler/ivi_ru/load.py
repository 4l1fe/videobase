# coding: utf-8
import requests
import parsers

HOST = 'www.ivi_ru.ru'
URL_SEARCH = 'search/ajax/new/autocomplete'


class IVI_LoadData(object):
    def __init__(self, film):
        self.resp_dict = {}
        self.film = film
        self.search_url = URL_SEARCH
        self.host = HOST
        self.params = {'q': self.film.name, 'json': 1, 'limit': 5}

    def __search(self, load_function):
        url = "http://%s/%s" % (self.host, self.search_url, )
        response = load_function(url, params=self.params)
        film = parsers.parse_search(response)
        if film is None:
            return False
        else:
            self.url_load = film['link']
            return True

    def load(self, load_function=requests.get):
        found = self.__search(load_function)
        if not found:
            return None
        url = "http://%s%s" % (self.host, self.url_load)
        return load_function(url, params=self.params)