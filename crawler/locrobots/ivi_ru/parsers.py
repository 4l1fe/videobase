# coding: utf-8
from crawler.core.parse import BaseParse
from crawler.core.exceptions import NoSuchFilm
from apps.contents.constants import *

from bs4 import BeautifulSoup
import re
import json


# Парсер для поисковика фильма
def parse_search(response, film):
    search_film = None
    try:
        js_films = json.loads(response)['content']
        for js_film in js_films:
            if js_film['year'] == film.release_date.year and\
               js_film['title'] == film.name:
                search_film = js_film
    except Exception as e:
        search_film = None
    return search_film


# Парсер для страницы фильма
class ParseFilmPage(BaseParse):
    def __init__(self, html):
        super(ParseFilmPage, self).__init__(html)
        self.soup = BeautifulSoup(html, "html")
        if self.soup.find_all('div', {'class': ['series-block']}):
            self.is_film = False
        else:
            self.is_film = True

    def get_link(self, **kwargs):
        link = self.soup.find_all('div', {'class':  'watch-top-main'})[0]\
            .find('div', {'class':  ['action-button-wrapper',
                                     'main-button-wrapper']})\
            .find('a')
        url = ''
        if link['href'] != '#':
            if '#' in link['href']:
                url = '%s%s' % (kwargs.get('url', ''), link['href'])
            else:
                url = link['href']
        else:
            #raise NoSuchFilm
            print "Film not found"
        return url

    def get_seasons(self, **kwargs):
        if not self.is_film:
            seasons_div_tag = self.soup.find_all('div', {'class': 'series-block'})
            seasons_number = seasons_div_tag.find('div', {'class': 'seasons-list-block'}).\
                find('li')
            return range(1, len(seasons_number)+1)
        else:
            return [0]

    def get_price(self, **kwargs):
        price = 0
        price_type = APP_CONTENTS_PRICE_TYPE_FREE
        root_div = self.soup.find('div', {'class': 'watch-top-main'})
        children_div = root_div.find('div', {'class': ['action-button-wrapper',
                                                        'main-button-wrapper']})
        if 'multi-choice' in children_div['class']:
            price_type = APP_CONTENTS_PRICE_TYPE_SUBSCRIPTION
            tag_label = children_div.find('label', {'for': "subscription-item-6"})
            reg = re.match(u'[a-zA-zа-яА-Я]*\d+[[a-zA-zа-яА-Я]*]', tag_label.text)
            price = float(reg)
        elif 'add_comming' in children_div['class']:
            price_type = APP_CONTENTS_PRICE_TYPE_FREE
            price = 0.0
        else:
            tag_a = children_div.find('a')
            price_type = APP_CONTENTS_PRICE_TYPE_PAY
            if 'data-can-buy' in tag_a.attrs:
                reg = re.findall(u'([0-9]+)', tag_a.text)
                price = float(reg[0])
            else:
                price_type = APP_CONTENTS_PRICE_TYPE_FREE
                price = 0.0

        return price, price_type

    def get_value(self, **kwargs):
        url = kwargs.get('url', None)
        if url is None:
            raise ValueError("Have not url to parse")
        chanks_url = url.split('/')
        index = chanks_url.index('watch')
        if index == -1:
            return ""
        else:
            return chanks_url[index + 1]

    def get_type(self, **kwargs):
        return 'ivi'



