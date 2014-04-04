# coding: utf-8
from ..core import BaseParse
from ..core.constants import *

from bs4 import BeautifulSoup
import json


# Парсер для поисковика фильма
def parse_search(response):
    try:
        films = json.loads(response.content)['content']
        search_film = films[0]
    except IndexError:
        search_film = None
    return search_film


# Парсер для страници фильма
class ParseFilmPage(BaseParse):
    def __init__(self, html):
        super(ParseFilmPage, self).__init__(html)
        self.soup = BeautifulSoup(html, "html")
        if self.soup.find_all('div', {'class': ['series-block']}):
            self.is_film = False
        else:
            self.is_film = True

    def get_link(self):
        link = self.soup.find_all('div', {'class':  'watch-top-main'})[0]\
            .find('div', {'class':  ['action-button-wrapper',
                                     'main-button-wrapper']})\
            .find('a')
        return None if link['href'] == '#' else link['href']

    def get_seasons(self):
        if not self.is_film:
            seasons_div_tag = self.soup.find_all('div', {'class': 'series-block'})
            seasons_number = seasons_div_tag.find('div', {'class': 'seasons-list-block'}).\
                find('li')
            return range(len(seasons_number))
        else:
            return [1]

    def get_price(self):
        price = 0
        price_type = APP_CRAWLER_PRICE_TYPE_FREE
        if self.is_film:
            root_div = self.soup.find_all('div', {'class': 'watch-top-main'})
            children_div = self.soup.find('div', {'class': 'action-button-wrapper main-button-wrapper'})
        return price, price_type

