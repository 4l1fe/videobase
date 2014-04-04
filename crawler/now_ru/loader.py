# coding: utf-8
import requests
import parsers
import urllib
from ..core import BaseLoader

HOST = 'www.now.ru'
URL_SEARCH = 'search?{}'
URL_LOAD = ''

class NOW_Loader(BaseLoader):
    def __init__(self, film, host=HOST, url_load=URL_LOAD):
        super(NOW_Loader, self).__init__(film, host, url_load)
        self.search_url = URL_SEARCH
        self.params = {'q': self.film.name}

    def get_url(self, load_function):
        url = "http://%s/%s" % (self.host, self.search_url)
        response = load_function(url, params=self.params)
        link = parsers.parse_search(response, self.film.name)
        if link is None:
            raise Exception()
        self.url_load = link
        return self.url_load


