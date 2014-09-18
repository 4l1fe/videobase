# coding: utf-8
from crawler.core import BaseParse
from apps.contents.constants import *
import re
from apps.films.constants import APP_FILM_FULL_FILM, APP_FILM_SERIAL
from bs4 import BeautifulSoup
import string

HOST = 'http://www.tvzor.ru'


def search_film(div, film_name, year):
    film_link = None
    if not (div is None):
        for item in div.find_all('div', {'class': 'vod'}):
            film_year = int(item.get('data-year'))
            if item.get('data-name').lower().strip().encode('utf-8').translate(None,
                                                                               string.punctuation) == film_name.lower().strip().encode(
                    'utf-8').translate(None, string.punctuation) and film_year == year:
                film_link = HOST + item.a.get('href')
                break
    return film_link


# Парсер для поисковика фильма
def parse_search(response, film_name, film_type, year):
    if not (type(film_name) is unicode):
        film_name = film_name.decode('utf-8')
    film_link = None
    try:
        soup = BeautifulSoup(response)
        if film_type == APP_FILM_FULL_FILM or film_type == u'':
            films_bloc = soup.find('div', {'data-id': 'movies-tab', 'class': 'tab-item'})
            film_link = search_film(films_bloc, film_name, year)
        elif film_type == APP_FILM_SERIAL:
            films_bloc = soup.find('ul', {'data-id': 'tvshows-tab', 'class': 'tab-item'})
            film_link = search_film(films_bloc, film_name, year)

    except IndexError:
        film_link = None
    return film_link


# Парсер для страници фильма
class ParseTvzorFilmPage(BaseParse):
    def __init__(self, html):
        super(ParseTvzorFilmPage, self).__init__(html)
        self.soup = BeautifulSoup(html, "html")

    def get_link(self, **kwargs):
        lnk = kwargs['url']
        if lnk:
            return lnk
        else:
            return ''

    def get_price(self, **kwargs):
        price = 0
        price_type = APP_CONTENTS_PRICE_TYPE_FREE
        price_button = self.soup.find('input', {'class': 'rent E'})
        if not price_button is None:
            price_type = APP_CONTENTS_PRICE_TYPE_PAY
            price = float(re.search(ur'\d+', price_button.get('value')).group())
        return price, price_type

    def get_seasons(self, **kwargs):
        seasons_div = self.soup.find('div', {'class': ['filters-area', 'new-navigation-module']})
        if seasons_div is not None:
            seasons = seasons_div.find_all('dt')
            return range(1, len(seasons) + 1)
        else:
            return [0]

    def get_type(self, **kwargs):
        return 'tvzorru'

    def get_value(self, **kwargs):
        pass
