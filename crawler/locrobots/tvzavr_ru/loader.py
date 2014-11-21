# coding: utf-8
from crawler.core import BaseLoader

HOST = 'http://www.tvzavr.ru'
URL_LOAD = ''


class Tvzavr_Loader(BaseLoader):
    def __init__(self, film, host=HOST, url_load=URL_LOAD):
        super(Tvzavr_Loader, self).__init__(film, host, url_load)
        self.search_url = 'http://www.tvzavr.ru/api/tvz/catalog?limit=200&offset=0'

    def get_url(self, load_function):
        return self.search_url

