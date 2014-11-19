# coding: utf-8
import copy
import string
import requests
from apps.contents.constants import APP_LOCATION_TYPE_ADDITIONAL_MATERIAL_FILM, \
    APP_LOCATION_TYPE_ADDITIONAL_MATERIAL_EPISODE, APP_LOCATION_TYPE_ADDITIONAL_MATERIAL_SEASON, \
    APP_CONTENTS_PRICE_TYPE_SUBSCRIPTION, APP_CONTENTS_PRICE_TYPE_PAY, APP_CONTENTS_PRICE_TYPE_FREE
from bs4 import BeautifulSoup
from apps.films.constants import APP_FILM_SERIAL
from crawler.core.exceptions import NoSuchFilm
from crawler.tor import simple_tor_get_page


class ParseTvzavrFilmPage(object):
    def __init__(self):
        pass

    def parse_data(self, film_name, film_year, serial, load_function):
        film_name = film_name.lower().strip().encode('utf-8').translate(None, string.punctuation)
        url = 'http://www.tvzavr.ru/api/tvz/catalog?limit=4000&offset=0'
        serial_list = []

        season_dict = {
            'season': '',
            'season_url': '',
            'episode_list': []
        }
        episode_dict = {
            'number': '',
            'url': '',
            'price': '',
            'price_type': ''
        }

        if serial:
            film_type = u'Сериалы'
        else:
            film_type = u'Фильмы'

        try:

            content = requests.get(url).content
            soup = BeautifulSoup(content, "xml")
            items = soup.findAll('item')

            for item in items:
                name = item.get('name').lower().strip().encode('utf-8').translate(None, string.punctuation)
                year = int(item.year.get('title'))
                category = item.category.get('title')

                if film_name == name and film_year == year and category == film_type:
                    film_url = item.get('url')
                    tariffs = item.findAll('tariff')

                    if len(tariffs) == 2:
                        price_dict = {
                            'price_subscription': int(item.find('tariff', {'type-alias': 'subscription'}).get('price')),
                            'price_purchase': int(item.find('tariff', {'type-alias': 'purchase'}).get('price'))
                        }
                    elif not item.find('tariff', {'type-alias': 'subscription'}) is None:
                        price_dict = {
                            'price_subscription': int(item.find('tariff', {'type-alias': 'subscription'}).get('price'))
                        }

                    elif not item.find('tariff', {'type-alias': 'purchase'}) is None:
                        price_dict = {
                           'price_purchase': int(item.find('tariff', {'type-alias': 'purchase'}).get('price'))
                        }

                    else:
                        price_dict = 0

                    if not serial:
                        return film_url, price_dict
                    else:
                        content = load_function(film_url)
                        soup = BeautifulSoup(content)
                        tags_a = soup.findAll('a', {'class': 'clip-link'})
                        season_dict['season_url'] = film_url
                        season_dict['season'] = 1

                        for tag_a in tags_a:
                            link = tag_a.get('href')

                            if u'Seriya' in link:
                                episode_dict['url'] = 'http://www.tvzavr.ru' + link
                                episode_dict['number'] = link.split('-')[3]

                                if 'price_purchase' in price_dict:
                                    episode_dict['price_type'] = APP_CONTENTS_PRICE_TYPE_PAY
                                    episode_dict['price']  = price_dict['price_purchase']

                                elif 'price_subscription' in price_dict:
                                    episode_dict['price_type'] = APP_CONTENTS_PRICE_TYPE_SUBSCRIPTION
                                    episode_dict['price'] = price_dict['price_subscription']

                                else:
                                    episode_dict['price_type'] = APP_CONTENTS_PRICE_TYPE_FREE
                                    episode_dict['price'] = 0

                                season_dict['episode_list'].append(copy.deepcopy(episode_dict))

                        serial_list.append(season_dict)
                        return serial_list, price_dict

        except Exception, e:
            print e
            return None

        return None

    def parse(self, response, dict_gen, film, url):
        serial = False

        if film.type == APP_FILM_SERIAL:
            serial = True

        urls, price_dict = self.parse_data(film.name, film.release_date.year, serial, simple_tor_get_page)

        if urls is None:
            raise NoSuchFilm(film)

        if 'price_purchase' in price_dict:
            price_type = APP_CONTENTS_PRICE_TYPE_PAY
            price = price_dict['price_purchase']
        elif 'price_subscription' in price_dict:
            price_type = APP_CONTENTS_PRICE_TYPE_SUBSCRIPTION
            price = price_dict['price_subscription']
        else:
            price_type = APP_CONTENTS_PRICE_TYPE_FREE
            price = 0

        resp_list = []
        if film.type == APP_FILM_SERIAL:
            for serial_season in urls:
                resp_dict = dict_gen(film)
                resp_dict['content_type'] = APP_LOCATION_TYPE_ADDITIONAL_MATERIAL_SEASON
                resp_dict['type'] = 'tvzavr'
                resp_dict['number'] = serial_season['season']
                resp_dict['value'] = ''
                resp_dict['url_view'] = serial_season['season_url']
                resp_dict['episode'] = 0
                resp_dict['price_type'] = price_type
                resp_dict['price'] = price

                resp_list.append(resp_dict)
                for episode in serial_season['episode_list']:
                    resp_dict = dict_gen(film)
                    resp_dict['content_type'] = APP_LOCATION_TYPE_ADDITIONAL_MATERIAL_EPISODE
                    resp_dict['type'] = 'tvzavr'
                    resp_dict['number'] = serial_season['season']
                    resp_dict['value'] = ''
                    resp_dict['url_view'] = episode['url']
                    resp_dict['price'] = episode['price']
                    resp_dict['price_type'] = episode['price_type']
                    resp_dict['episode'] = episode['number']
                    resp_list.append(resp_dict)
        else:
            resp_dict = dict_gen(film)
            resp_dict['type'] = 'tvzavr'
            resp_dict['number'] = 0
            resp_dict['value'] = ''
            resp_dict['url_view'] = urls
            resp_dict['price'] = price
            resp_dict['content_type'] = APP_LOCATION_TYPE_ADDITIONAL_MATERIAL_FILM
            resp_dict['episode'] = 0
            resp_dict['price_type'] = price_type
            resp_list.append(resp_dict)

        return resp_list

    def get_price(self):
        return 79

    def get_seasons(self):
        return [0, ]

    def get_link(self):
        return ''