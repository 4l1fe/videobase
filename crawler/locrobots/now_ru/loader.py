# coding: utf-8
from crawler.core.exceptions import NoSuchFilm
import parsers
import urllib
from crawler.core import BaseLoader
from utils.common import url_with_querystring

HOST = 'www.now.ru'
URL_SEARCH = 'search'
URL_LOAD = ''


class NOW_Loader(BaseLoader):
    def __init__(self, film, host=HOST, url_load=URL_LOAD):
        super(NOW_Loader, self).__init__(film, host, url_load)
        self.search_url = URL_SEARCH
        self.params = {'q': self.film.name}

    def get_url(self, load_function):
        url = "http://%s/%s" % (self.host, self.search_url)
        url = url_with_querystring(url, **self.params)
        response = load_function(url)
        link = parsers.parse_search(response, self.film.name, self.film.release_date.year)
        if link is None:
            raise NoSuchFilm(self.film)
        self.url_load = link
        return self.url_load


