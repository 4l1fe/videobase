# coding: utf-8
from apps.contents.constants import *
from bs4 import BeautifulSoup
from crawler.core import BaseParse
import re


def parse_search(response, film_name):
    film_link = None
    try:
        content = response.content
        soup = BeautifulSoup(content)
        if not (soup.find('div', {'class': 'empty-search'}) is None):
            return None
        search_div = soup.find('div', {'class': 'card-list'})
        film_divs = search_div.find_all('div', {'class': ['card', 'no-rationale', 'tall-cover', 'movies tiny']})
        for film in film_divs:
            film_tag = film.find('a', {'class': 'title'})
            if film_name == film_tag.get('title'):
                film_link = 'http://play.google.com' + film_tag.get('href')
    except IndexError:
        film_link = None
    return film_link


class ParsePlayGoogleFilm(BaseParse):
    def __init__(self, html):
        super(ParsePlayGoogleFilm, self).__init__(html)
        self.soup = BeautifulSoup(html, "html")

    def get_link(self, **kwargs):
        return kwargs['url']

    def get_price(self, **kwargs):
        price_type = APP_CONTENTS_PRICE_TYPE_PAY
        button_price = self.soup.find('button', {'class': ['price', 'buy']})
        try:
            list_spans = button_price.find_all('span', {'itemprop': 'offers'})
            price_span = list_spans[len(list_spans)-1]
            price_tag = price_span.find(itemprop='price')
            reg = re.search(ur'\d+', price_tag.get('content'))
            price = float(reg.group())
        except:
            return 0, APP_CONTENTS_PRICE_TYPE_FREE
        return price, price_type

    def get_seasons(self, **kwargs):
         return [0]

    def get_type(self, **kwargs):
        return 'playgoogle'