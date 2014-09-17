# coding: utf-8
import json
from apps.contents.constants import *
from bs4 import BeautifulSoup
from crawler.core import BaseParse
import re
import string


def parse_search(response, film_name):
    film_link = None
    try:
        flag = False
        soup = BeautifulSoup(response)
        if soup.find(attrs={'data-href': 'video_search'}) is None:
            return None
        class_tag = soup.find('aside', {'role': 'complementary'})

        if class_tag:
            li_list = class_tag.find_all('li')
            for li in li_list:
                if u'Видео' in li.text:
                    flag = True
                    break
        if flag:
            search_divs = soup.find_all('div', {'class': 'catalog-list search'})
            film_div = None
            for div in search_divs:
                if div.figure:
                    film_div = div
                    break
            if film_div:
                films = film_div.find_all('figure')
                for film in films:
                    if film_name.lower().strip().encode('utf-8').translate(None, string.punctuation) == film.figcaption.div.header.strong.text.lower().strip().encode('utf-8').translate(None, string.punctuation):
                        film_link = 'http://www.zabava.ru' + film.a.get('href')
                        break
            else:
                return None
        else:
            return None
    except:
        film_link = None
    return film_link


class ParseZabavaFilm(BaseParse):
    def __init__(self, html):
        super(ParseZabavaFilm, self).__init__(html)
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

    def get_type(self, **kwargs):
        return 'zabavaru'

    def get_value(self, **kwargs):
        pass