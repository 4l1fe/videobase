# coding: utf-8
from apps.contents.constants import *
from bs4 import BeautifulSoup
from crawler.core import BaseParse
from apps.films.constants import APP_FILM_FULL_FILM, APP_FILM_SERIAL
import re
import string


def search_film(ul, film_name, year):
    film_link = None
    if not (ul is None):
        for li in ul.select('li.item'):
            div = li.find(class_='description')
            tag_year = div.find('p', {'class':'genre-year'}).text
            film_year = int(re.search(ur'\d+', tag_year).group())
            if div.a.text.lower().strip().encode('utf-8').translate(None, string.punctuation) == film_name.lower().strip().encode('utf-8').translate(None, string.punctuation) and film_year == year:
                film_link = 'http://www.stream.ru' + div.a.get('href')
                break

    return film_link


def parse_search(response, film_name, film_type, year):
    film_link = None
    try:
        soup = BeautifulSoup(response)
        if not (soup.find(attrs={'class': 'found-nothing'}) is None):
            return None
        if film_type == APP_FILM_FULL_FILM or film_type == u'':
            ul = soup.find('ul', {'class': 'item-list'})
            film_link = search_film(ul, film_name, year)
        elif film_type == APP_FILM_SERIAL:
            ul = soup.find('ul', {'class': 'item-list2'})
            film_link = search_film(ul, film_name, year)
    except IndexError:
        film_link = None
    return film_link


class ParseStreamFilm(BaseParse):
    def __init__(self, html):
        super(ParseStreamFilm, self).__init__(html)
        self.soup = BeautifulSoup(html, "html")

    def search_price(self, price_li, price_type):
        span_price = price_li.find('span', {'class': 'price'})
        p_type = price_type
        reg = re.search(ur'\d+', span_price.text)
        price = float(reg.group())
        return price, p_type

    def get_link(self, **kwargs):
        lnk = kwargs['url']
        if lnk:
            return lnk
        else:
            return ''

    def get_price(self, **kwargs):
        price = 0
        price_type = APP_CONTENTS_PRICE_TYPE_FREE
        price_li = self.soup.find('li', {'class': ['watch', 'buy_rent']})
        if price_li != None:
            return self.search_price(price_li, APP_CONTENTS_PRICE_TYPE_PAY)
        else:
            price_li = self.soup.find('li', {'class': 'subscribe'})
            if price_li != None:
                return self.search_price(price_li, APP_CONTENTS_PRICE_TYPE_SUBSCRIPTION)
            else:
                price_li = self.soup.find('li', {'class': 'buy'})
                if price_li != None:
                    return self.search_price(price_li, APP_CONTENTS_PRICE_TYPE_PAY)
        return price, price_type

    def get_seasons(self, **kwargs):
        seasons_ul = self.soup.find('ul', {'class': 'seasons'})
        if seasons_ul != None:
            seasons_li = seasons_ul.find_all('li')
            return range(1, len(seasons_li) + 1)
        else:
            return [0]

    def get_type(self, **kwargs):
        return 'streamru'

    def get_value(self, **kwargs):
        pass