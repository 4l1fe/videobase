# coding: utf-8
import json
from apps.contents.constants import *
from bs4 import BeautifulSoup
from crawler.core import BaseParse
import re


def parse_search(response, film_name):
    film_link = None
    try:
        content = response.content
        soup = BeautifulSoup(content)
        if soup.find(attrs={'data-href': 'video_search'}) is None:
            return None
        search_divs = soup.find_all('div', {'class': ['catalog-list', 'search']})
        for div in search_divs:
            if div.figure:
                film_div = div
        films = film_div.find_all('figure')
        for film in films:
            if film_name == film.figcaption.div.header.strong.text:
                film_link = 'http://www.zabava.ru' + film.a.get('href')
                break
    except:
        film_link = None
    return film_link


class ParseZabavaFilm(BaseParse):
    def __init__(self, html):
        super(ParseZabavaFilm, self).__init__(html)
        self.soup = BeautifulSoup(html, "html")

    def get_link(self, **kwargs):
        return kwargs['url']

    def get_price(self, **kwargs):
        price = 0
        price_type = APP_CONTENTS_PRICE_TYPE_FREE
        price_ul = self.soup.find('ul', {'class': 'btn-group-list'})
        season_div = self.soup.find('div', {'class': 'season mbottom20'})
        try:
            if season_div:
                price_data = season_div.find('a', {'class': 'btn-buy'}).get('data-value')
            else:
                price_lis = price_ul.find_all('li')
                if len(price_lis) > 1:
                    for li in price_lis:
                        if re.search(u'Напрокат', li.a.text):
                            price_li = li
                            break
                else:
                    price_li = price_lis[0]
                price_data = price_li.a.get('data-value')
            if price_data:
                price = float(json.loads(price_data)['price'])
                price_type = APP_CONTENTS_PRICE_TYPE_PAY
        except:
            return price, price_type
        return price, price_type

    def get_seasons(self, **kwargs):
        seasons_div = self.soup.find('div', {'class': 'span12 seasons'})
        if not(seasons_div is None):
            seasons_ul = seasons_div.find_all('ul')
            return range(1, len(seasons_ul) + 1)
        else:
            return [0]