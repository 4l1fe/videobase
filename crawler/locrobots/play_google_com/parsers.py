# coding: utf-8
from apps.contents.constants import *
from bs4 import BeautifulSoup
from crawler.core import BaseParse
import re
import string
from crawler.tor import simple_tor_get_page


def parse_search(response, film_name, year):
    film_link = None
    try:
        soup = BeautifulSoup(response)
        if not (soup.find('div', {'class': 'empty-search'}) is None):
            return None
        search_div = soup.find('div', {'class': 'card-list'})
        film_divs = search_div.find_all('div', {'class': ['card', 'no-rationale', 'tall-cover', 'movies tiny']})
        for film in film_divs:
            film_tag = film.find('a', {'class': 'title'})
            if film_name.lower().strip().encode('utf-8').translate(None, string.punctuation) == film_tag.get('title').lower().strip().encode('utf-8').translate(None, string.punctuation):
                film_link = 'http://play.google.com' + film_tag.get('href')
        if film_link:
            page = simple_tor_get_page(film_link)
            soup_page = BeautifulSoup(page)
            film_year = soup_page.find('div', {'itemprop':'datePublished'}).text
            film_year = re.search(ur'\d+', film_year)
            if not str(year) in film_year.group():
                return None
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

    def get_value(self, **kwargs):
        pass