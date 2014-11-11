# coding: utf-8
import copy
import string
from apps.contents.constants import APP_LOCATION_TYPE_ADDITIONAL_MATERIAL_EPISODE, \
    APP_LOCATION_TYPE_ADDITIONAL_MATERIAL_SEASON, APP_LOCATION_TYPE_ADDITIONAL_MATERIAL_FILM
from apps.films.constants import APP_FILM_FULL_FILM, APP_FILM_SERIAL
from bs4 import BeautifulSoup
from crawler.core.exceptions import NoSuchFilm
from crawler.tor import simple_tor_get_page
import requests

HOST = 'http://www.zoomby.ru'


class ParseFilm(object):
    def __init__(self):
        self.parse_value = 'http://www.zoomby.ru/v/'

    def data_parse(self, film_name, year, load_function, ser):
        film_name = film_name.lower().strip().encode('utf-8').translate(None, string.punctuation)
        serial_list = []
        season_dict = {
            'season': '',
            'season_url': '',
            'episode_list': ''
        }
        episode_dict = {
            'number': '',
            'url': ''
        }
        try:
            i = 1
            if ser:
                url = 'http://www.zoomby.ru/series?offset=0&p={page}'
            else:
                url = 'http://www.zoomby.ru/films?offset=0&p={page}'

            while 1:
                link = url.format(page=i)
                data_dict = requests.get(link).json()

                if not data_dict['success']:
                    return None

                for serial in data_dict['catalog']:
                    name = serial['title'].lower().strip().encode('utf-8').translate(None, string.punctuation)
                    if film_name == name and year == int(serial['year']):
                        season_url = HOST + serial['url']
                        season_dict['season_url'] = season_url
                        if ser:
                            response = load_function(season_url)
                            soup = BeautifulSoup(response)
                            tags_li = soup.find('ul', {'class': 'panel01ul'}).findAll('li')
                            episode_list = []
                            for li in tags_li:
                                season_dict['season'] = 1
                                serial_text = li.find('strong', {'class': 'row1long'}).text
                                if u'серия' in serial_text:
                                    episode_dict['number'] = int(serial_text.split('-')[0])
                                    episode_dict['url'] = HOST + '/watch/' + li.a.get('href')
                                    episode_list.append(copy.deepcopy(episode_dict))
                            season_dict['episode_list'] = episode_list
                            serial_list.append(season_dict)
                            return serial_list
                        else:
                            return season_url
                i += 1
        except Exception:
            film_link = None
        return film_link

    def parse(self, response, dict_gen, film, url):
        serial = False

        if film.type == APP_FILM_SERIAL:
            serial = True


        serial_list = self.data_parse(film.name, film.release_date.year, simple_tor_get_page, serial)

        if serial:
            content = simple_tor_get_page(serial_list[0]['season_url'])
        else:
            content = simple_tor_get_page(serial_list)

        if serial_list is None:
            raise NoSuchFilm(film)

        value = ''
        resp_list = []
        try:
            soup = BeautifulSoup(content)
            tag = soup.find('meta', attrs={'property': 'og:type'})
            if (not tag is None and film.type == APP_FILM_FULL_FILM)\
                    or (film.type == APP_FILM_SERIAL and tag is None):
                tag = soup.find('div', attrs={'class': 'big_rating'})
                id = tag.get('id')
                value = self.parse_value + id

        except Exception:
            pass

        if film.type == APP_FILM_SERIAL:
            for serial_season in serial_list:
                resp_dict = dict_gen(film)
                resp_dict['content_type'] = APP_LOCATION_TYPE_ADDITIONAL_MATERIAL_SEASON
                resp_dict['type'] = 'zoomby'
                resp_dict['number'] = serial_season['season']
                resp_dict['value'] = value
                resp_dict['url_view'] = serial_season['season_url']
                resp_dict['price'] = self.get_price()
                resp_list.append(resp_dict)
                for episode in serial_season['episode_list']:
                    resp_dict = dict_gen(film)
                    resp_dict['content_type'] = APP_LOCATION_TYPE_ADDITIONAL_MATERIAL_EPISODE
                    resp_dict['type'] = 'zoomby'
                    resp_dict['number'] = serial_season['season']
                    resp_dict['value'] = value
                    resp_dict['url_view'] = episode['url']
                    resp_dict['price'] = self.get_price()
                    resp_dict['episode'] = episode['number']
                    resp_list.append(resp_dict)
        else:
            resp_dict = dict_gen(film)
            resp_dict['type'] = 'tvigle'
            resp_dict['number'] = 0
            resp_dict['value'] = value
            resp_dict['url_view'] = serial_list
            resp_dict['price'] = self.get_price()
            resp_dict['content_type'] = APP_LOCATION_TYPE_ADDITIONAL_MATERIAL_FILM
            resp_list.append(resp_dict)

        return resp_list

    def get_price(self):
        return 0

    def get_seasons(self):
        return self.serial_list
