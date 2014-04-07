# coding: utf-8
from crawler.core.exceptions import NoSuchFilm
import requests
import parsers
from ..core import BaseLoader
import urllib

HOST = 'www.tvigle.ru'
URL_LOAD = ''



class TVIGLE_Loader(BaseLoader):
    def __init__(self, film, host=HOST, url_load=URL_LOAD):
        super(TVIGLE_Loader, self).__init__(film, host, url_load)
        self.search_url = 'category/search/?{}'.format(urllib.urlencode({'search_text':(self.film.name.encode('cp1251'))}))



    def get_url(self, load_function):
        url = "http://%s/%s" % (self.host, self.search_url, )
        response = load_function(url)
        filmLink = parsers.parse_search(response,self.film.name)
        if filmLink is None:
            raise NoSuchFilm(self.film)
        self.url_load = filmLink
        return "http://%s%s" % (self.host, self.url_load)