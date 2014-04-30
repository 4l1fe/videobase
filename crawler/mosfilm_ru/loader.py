# coding: utf-8
import urllib
from crawler.core import BaseLoader
URL_LOAD = ''
HOST = 'http://www.mosfilm.ru'


class Mosfilm_Loader(BaseLoader):
    def __init__(self, film, host=HOST, url_load=URL_LOAD):
        super(Mosfilm_Loader, self).__init__(film, host, url_load)
        self.url_serch = 'search/?{}'.format(urllib.urlencode({'b_search_words': u'Девчата', 'p_f_1_title': u'Девчата', 'p_f_2_title': u'Девчата'}))

    def get_url(self, load_function):
        print self.url_serch
