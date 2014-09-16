# coding: utf-8
from crawler.core.parse import BaseParse
from crawler.core.exceptions import NoSuchFilm
from apps.contents.constants import *

from bs4 import BeautifulSoup
import re
import json


# Парсер для поисковика фильма
def parse_search(response, film):
    search_film_url = None
    try:
        soup = BeautifulSoup(response)
        video_view = soup.find('div', {'id': 'placenta'}).find('div', {'class': 'video_view'})
        items = soup.find('div', {'id': 'placenta'}).find('div', { "class" : "list_videos_all" })
        if video_view:
            name = unicode(video_view.find('h1').find('span').contents[0])
            block_content = video_view.find('div', {'class': 'block_content'})
            all_p_tags = block_content.findAll('p')
            year = None
            for p in all_p_tags:
                b = p.find('b')
                if b and unicode(b.contents[0]) == u'Год':
                    year = int(p.find('a').contents[0])
                    break
            if year == film.release_date.year and name == film.name:
                search_film_url = soup.head.find('link', rel='canonical').get('href')

        elif items:
            for item_div in items.findAll('div', { "class" : "item" }):
                item_info = item_div.find('div', { "class" : "info" })
                a = item_info.find('h3').find('a')
                name = unicode(a.contents[0])
                year = int(item_info.find('h4').contents[0])
                if year == film.release_date.year and name == film.name:
                    search_film_url = a.get('href')
                    break

    except Exception as e:
        print e
        search_film_url = None

    return search_film_url


# Парсер для страницы фильма
class ParseVIDEOMAXPage(BaseParse):
    def __init__(self, html):
        super(ParseVIDEOMAXPage, self).__init__(html)
        self.soup = BeautifulSoup(self.html)

    def get_link(self, **kwargs):
        link = self.soup.head.find('link', rel='canonical').get('href')
        if link:
            return link
        else:
            return ''

    def get_seasons(self, **kwargs):
        try:
            has_seasons = unicode(self.soup.find('div', {'id': 'placenta'}).find('div', {'class': 'list_dvds'}).find('div', {'class': 'block_header'}).contents[0])
            if has_seasons == u'Все сезоны':
                seasons_block_content = self.soup.find('div', {'class': 'list_dvds'}).find('div', {'class': 'block_content'})
                season_items = seasons_block_content.findAll('div', {'class': 'item'})
                return range(1, len(season_items)+1)
        except Exception:
            pass

        return [0]

    def get_price(self, **kwargs):
        price_type = APP_CONTENTS_PRICE_TYPE_FREE
        price = 0.0
        return price, price_type

    def get_value(self, **kwargs):
        link = self.soup.head.find('link', rel='canonical').get('href')
        return link

    def get_type(self, **kwargs):
        return 'videomax'



