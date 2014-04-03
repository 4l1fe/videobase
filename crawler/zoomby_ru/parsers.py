# coding: utf-8
from ..core import BaseParse
from bs4 import BeautifulSoup
from social.backends.ubuntu import UbuntuOpenId

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



class ParseFilm(BaseParse):
    def __init__(self):
        self.host = HOST
        self.url_film = URL_FILM

    def get_price(self):
        return 0

    def get_seasons(self):
        return 1

    def get_link(self):
        return URL_FILM

