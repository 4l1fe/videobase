# coding: utf-8
from crawler.core.exceptions import NoSuchFilm
import string
import parsers
import re
from crawler.core import BaseLoader
from utils.common import url_with_querystring

HOST = 'www.megogo.net/ru'
URL_SEARCH = 'searchhint'
URL_LOAD = ''


class MEGOGO_Loader(BaseLoader):
    def __init__(self,  film, host=HOST, url_load=URL_LOAD):
        super(MEGOGO_Loader, self).__init__(film, host, url_load)
        self.search_url = URL_SEARCH
        self.params = {'lang': 'ru', 'q': re.sub('[' + string.punctuation + ']', '', self.film.name).lower().strip()}

    def get_url(self, load_function):
        url = "http://%s/%s" % (self.host, self.search_url, )
        url = url_with_querystring(url, **self.params)
        response = load_function(url)
        film = parsers.parse_search(response, self.film.name, self.film.release_date.year)
        if film is None:
            raise NoSuchFilm(self.film)
        self.url_load = film['view_link']
        return self.url_load