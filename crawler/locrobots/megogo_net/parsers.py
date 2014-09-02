# coding: utf-8
from crawler.core import BaseParse
from bs4 import BeautifulSoup
from apps.contents.constants import *
import string
import re
import json


def parse_search(response, filmName, year):
    regFilmname = re.compile('(?P<name>.+)[ ][(](?P<year>[0-9]{4})[)]')
    search_film = None
    try:
        films = json.loads(response)
        for film in films:
            search = regFilmname.search(film['title'])
            if search.group('name').lower().strip().encode('utf-8').translate(None, string.punctuation) == filmName.lower().strip().encode('utf-8').translate(None, string.punctuation) and str(year) in search.group('year'):
                search_film = film
                break
    except IndexError:
        search_film = None
    return search_film


class ParseMegogoFilm(BaseParse):
    def __init__(self, html):
        super(ParseMegogoFilm, self).__init__(html)
        self.soup = BeautifulSoup(html, "html")

    def get_link(self, **kwargs):
        filmLinkDiv =  self.soup.find('div', {'class': 'fb-like'})
        return filmLinkDiv.get('data-href')

    def get_price(self, **kwargs):
        price = 0
        price_type = APP_CONTENTS_PRICE_TYPE_FREE
        rootDiv = self.soup.find('div', {'class': 'view-wide'})
        aPrice = rootDiv.find('a', {'id': 'paymentBuyLink'})
        if aPrice != None:
            price_type = APP_CONTENTS_PRICE_TYPE_PAY
            reg = re.search(ur'\d+', aPrice.text)
            price = float(reg.group())
        else:
            aPrice = rootDiv.find('a', {'id': 'paymentSubscribeLink'})
            if aPrice != None:
                price_type = APP_CONTENTS_PRICE_TYPE_SUBSCRIPTION
        return price, price_type

    def get_seasons(self, **kwargs):
        seasonsUl = self.soup.find('ul', {'class': 'seasons_list'})
        if seasonsUl != None:
            seasonsLi = seasonsUl.find_all('li')
            return range(1, len(seasonsLi)+1)
        else:
            return [0]

    def get_type(self, **kwargs):
        return 'megogo'

    def get_value(self, **kwargs):
        pass

