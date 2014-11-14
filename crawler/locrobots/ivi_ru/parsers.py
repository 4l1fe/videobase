# coding: utf-8
from apps.contents.constants import *
from apps.films.constants import APP_FILM_SERIAL
from crawler.core.parse import BaseParse

import re
import json
import requests
from bs4 import BeautifulSoup


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
    def __init__(self, html, film):
        super(ParseFilmPage, self).__init__(html, film)
        self.soup = BeautifulSoup(html, "html")
        self.host = "http://www.ivi.ru"

    def get_link(self, **kwargs):
        ret_value = None
        if self.film_type == APP_FILM_SERIAL:
            seasons = self._get_seasons(url=kwargs.get('url'))
            ret_value = self._get_series(seasons)
        else:
            link = self.soup.find_all('div', {'class':  'watch-top-main'})[0]\
                .find('div', {'class':  ['action-button-wrapper',
                                         'main-button-wrapper']})\
                .find('a')
            ret_value = ''
            if link['href'] != '#':
                if '#' in link['href']:
                    ret_value = '%s%s' % (kwargs.get('url', ''), link['href'])
                else:
                    ret_value = link['href']
            else:
                #raise NoSuchFilm
                print "Film not found"

        return ret_value

    def _get_seasons(self, url):
        seasons_list = []
        seasons_div = self.soup.find('div', {'class': 'series-block'})
        if seasons_div:
            seasons_tag = seasons_div.select("div.seasons-list-block li a")
            if seasons_tag:
                for season in seasons_tag:
                    seasons_list.append({
                        'id': season['data-compilation'],
                        'season_numer': season['data-season'],
                        'season_url': "{0}{1}".format(self.host, season['href'])
                    })
            else:
                recomend_tag = self.soup.find('div', {'id': 'video_block_recomendations'})
                seasons_list.append({
                    'id': recomend_tag['data-compilation-id'],
                    'season_numer': 0,
                    'season_url': url,
                })
        else:
            print "This film is not a serial"
        return seasons_list

    def _get_series(self, seasons_list):
        url = "{0}/{1}".format(self.host, "video/json/video/items")
        params = {'limit': "", 'ids[]': "", 'action': 'series', 'tmpl': 0}
        series = []
        for season in seasons_list:
            params['ids[]'] = season['id']
            params['limit'] = season['season_numer']
            data = requests.get(url, params=params)
            series.append({'season': season['season_numer'],
                           'season_url': season['season_url'],
                           'episode_list': [
                               {'season': episode['season'] if episode['season'] else 1,
                                'url': "{0}{1}".format(self.host, episode['url']),
                                'number': episode['episode']}
                               for episode in data.json()]})
        return series

    def get_seasons(self, **kwargs):
        pass

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