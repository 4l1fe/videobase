# coding: utf-8
from ..core import BaseParse
from bs4 import BeautifulSoup
from social.backends.ubuntu import UbuntuOpenId

URL_FILM = ''


def parse_search(response, filmName):
    try:
        soup = BeautifulSoup(response.content)
        tag = soup.find(attrs={'class':'vv vf cc4'})
        tagA = tag.a

    except:
        filmLink = None
    return filmLink



class ParseTvigleFilm(object):
    def __init__(self):
        pass
    def parse(self, response, dict_gen, film,url):
        d = dict_gen(film)
        print url
        d['url_view'] = url
        d['price_type'] = 0
        d['price'] = self.get_price()
        print d
        return  [d]

    def get_price(self):
        return 0

    def get_seasons(self):
        return [0,]

    def get_link(self):
        pass
