# coding: utf-8
import json
from apps.contents.constants import *
from bs4 import BeautifulSoup
from crawler.core import BaseParse

def parse_search(response, film_name):
    film_link = None
    try:
        films = json.loads(response.content)['live_search']['search_movies_result']
        for film in films:
            if film['rus_title'] == film_name:
                film_link = 'https://ayyo.ru/movies/%s/' % (film['slug'])
                break
        # if not (soup.find('div', {'class': 'empty-search'}) is None):
        #     return None
        # search_div = soup.find('div', {'class': 'card-list'})
        # film_divs = search_div.find_all('div', {'class': ['card', 'no-rationale', 'tall-cover', 'movies tiny']})
        # for film in film_divs:
        #     film_tag = film.find('a', {'class': 'title'})
        #     if film_name == film_tag.get('title'):
        #         film_link = 'http://play.google.com' + film_tag.get('href')
    except IndexError:
        film_link = None
    return film_link


class ParseAyyoFilms(BaseParse):
    def __init__(self, html):
        super(ParseAyyoFilms, self).__init__(html)
        self.soup = BeautifulSoup(html, "html")

    def get_link(self, **kwargs):
        return kwargs['url']

    def get_price(self, **kwargs):
        price_type = APP_CONTENTS_PRICE_TYPE_PAY
        print self.soup
        div_price = self.soup.find('div', {'class': 'bPurchaseButton'})
        price = float(div_price.get('data-movie-price'))
        print '!'
        # try:
        #     list_spans = button_price.find_all('span', {'itemprop': 'offers'})
        #     price_span = list_spans[len(list_spans)-1]
        #     price_tag = price_span.find(itemprop='price')
        #     reg = re.search(ur'\d+', price_tag.get('content'))
        #     price = float(reg.group())
        # except:
        #     return 0, APP_CONTENTS_PRICE_TYPE_FREE
        return price, price_type

    def get_seasons(self, **kwargs):
         return [0]