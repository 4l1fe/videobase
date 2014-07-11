# coding: utf-8
import urllib
from apps.films.constants import APP_FILM_SERIAL
from crawler.core import BaseLoader
from crawler.core.exceptions import NoSuchFilm
from crawler.oll_tv.parser import ParseOllFilm

HOST = 'www.oll.tv'
URL_LOAD = ''


class Oll_Loader(BaseLoader):
    def __init__(self, film, host=HOST, url_load=URL_LOAD):
        super(Oll_Loader, self).__init__(film, host, url_load)
        self.search_url = 'search?{}'.format(urllib.urlencode({'q': self.film.name.encode('utf-8')}))

    def get_url(self, load_function):
        url = "http://%s/%s" % (self.host, self.search_url, )
        return url
