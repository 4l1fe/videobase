# coding: utf-8
import string
import requests
from apps.contents.constants import  APP_LOCATION_TYPE_ADDITIONAL_MATERIAL_FILM, \
    APP_LOCATION_TYPE_ADDITIONAL_MATERIAL_EPISODE, APP_LOCATION_TYPE_ADDITIONAL_MATERIAL_SEASON
from bs4 import BeautifulSoup
from apps.films.constants import APP_FILM_SERIAL
from crawler.core.exceptions import NoSuchFilm


class ParseTvzavrFilmPage(object):
    def __init__(self):
        pass

    def parse_data(self, film_name, film_year, serial):
        film_name = film_name.lower().strip().encode('utf-8').translate(None, string.punctuation)
        offset = 0
        url = 'http://www.tvzavr.ru/api/tvz/catalog?limit=200&offset={offset}'

        if serial:
            film_type = u'Сериалы'
        else:
            film_type = u'Фильмы'

        try:
            while offset < 4000:
                url = url.format(offset=offset)
                offset += 200
                content = requests.get(url).content
                soup = BeautifulSoup(content)
                items = soup.findAll('item')

                for item in items:
                    name = item.get('name').lower().strip().encode('utf-8').translate(None, string.punctuation)
                    year = int(item.year.get('title'))
                    category = item.category.get('title')

                    if film_name == name and film_year == year and category == film_type:
                        film_url = item.get('url')
                        if not serial:
                            return film_url
                        else:
                            pass

        except Exception:
            return None

        return None

    def parse(self, response, dict_gen, film, url):
        serial = False

        if film.type == APP_FILM_SERIAL:
            serial = True

        urls = self.parse_data(film.name, film.release_date.year, serial)

        if urls is None:
            raise NoSuchFilm(film)

        resp_list = []
        if film.type == APP_FILM_SERIAL:
            for serial_season in urls:
                resp_dict = dict_gen(film)
                resp_dict['content_type'] = APP_LOCATION_TYPE_ADDITIONAL_MATERIAL_SEASON
                resp_dict['type'] = 'tvzavr'
                resp_dict['number'] = serial_season['season']
                resp_dict['value'] = ''
                resp_dict['url_view'] = serial_season['season_url']
                resp_dict['price'] = self.get_price()
                resp_dict['episode'] = 0
                resp_list.append(resp_dict)
                for episode in serial_season['episode_list']:
                    resp_dict = dict_gen(film)
                    resp_dict['content_type'] = APP_LOCATION_TYPE_ADDITIONAL_MATERIAL_EPISODE
                    resp_dict['type'] = 'tvzavr'
                    resp_dict['number'] = serial_season['season']
                    resp_dict['value'] = ''
                    resp_dict['url_view'] = episode['url']
                    resp_dict['price'] = self.get_price()
                    resp_dict['episode'] = episode['number']
                    resp_list.append(resp_dict)
        else:
            resp_dict = dict_gen(film)
            resp_dict['type'] = 'tvzavr'
            resp_dict['number'] = 0
            resp_dict['value'] = ''
            resp_dict['url_view'] = urls
            resp_dict['price'] = self.get_price()
            resp_dict['content_type'] = APP_LOCATION_TYPE_ADDITIONAL_MATERIAL_FILM
            resp_dict['episode'] = 0
            resp_list.append(resp_dict)

        return resp_list

    def get_price(self):
        return 79

    def get_seasons(self):
        return [0, ]

    def get_link(self):
        return ''