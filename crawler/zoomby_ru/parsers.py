# coding: utf-8

from ..core import BaseParse
from bs4 import BeautifulSoup

URL_FILM = ''
HOST = 'http://www.zoomby.ru'

def parse_search(response, filmName):
    try:
        soup = BeautifulSoup(response.content)
        tag = soup.find(attrs={'class':'element_row_3'},text=filmName)
        tagA = tag.a
        filmLink = tagA.get('href')
        URL_FILM = HOST + filmLink
    except:
        filmLink = None
    return filmLink



class ParseFilm(object):
    def __init__(self):
        pass
    def parse(self, response, dict_gen, film,url):
        d = dict_gen(film)
        d['url_view'] = url
        d['price_type'] = 0
        d['price'] = self.get_price()
        return [d]

    def get_price(self):
        return 0

    def get_seasons(self):
        return [0, ]

    def get_link(self):
        pass

