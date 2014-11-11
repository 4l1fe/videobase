# coding: utf-8
from crawler.core import BaseLoader

HOST = 'www.zoomby.ru'
URL_LOAD = ''


class ZOOMBY_Loader(BaseLoader):
    def __init__(self, film, host=HOST, url_load=URL_LOAD):
        super(ZOOMBY_Loader, self).__init__(film, host, url_load)
        self.search_url = 'http://www.zoomby.ru/films?offset=0&p=1'

    def get_url(self, load_function):
        return self.search_url
