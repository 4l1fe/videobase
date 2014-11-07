# coding: utf-8
import string
from apps.contents.constants import APP_LOCATION_TYPE_ADDITIONAL_MATERIAL_EPISODE, \
    APP_LOCATION_TYPE_ADDITIONAL_MATERIAL_SEASON, APP_LOCATION_TYPE_ADDITIONAL_MATERIAL_FILM
from apps.films.constants import APP_FILM_FULL_FILM, APP_FILM_SERIAL
from bs4 import BeautifulSoup
from crawler.tor import simple_tor_get_page
import requests

HOST = 'http://www.zoomby.ru'


class ParseFilm(object):
    def __init__(self):
        self.parse_value = 'http://www.zoomby.ru/v/'

    @classmethod
    def parse_search(cls, film_name, year, load_function, ser):
        film_name = film_name.lower().strip().encode('utf-8').translate(None, string.punctuation)
        cls.serial_list = []
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
                        cls.season_url = HOST + serial['url']
                        season_dict['season_url'] = cls.season_url
                        if ser:
                            response = load_function(cls.season_url)
                            soup = BeautifulSoup(response)
                            tags_li = soup.find('ul', {'class': 'panel01ul'}).findAll('li')
                            for li in tags_li:
                                serial_text = li.find('strong', {'class': 'row1long'}).text
                                if u'серия' in serial_text:
                                    episode_dict['number'] = int(serial_text.split('-')[0])
                                    episode_dict['url'] = HOST + '/' + li.a.get('href')
                                    season_dict['season'] = 1
                                    season_dict['episode_list'] = season_dict
                                    cls.serial_list.append(season_dict)
                            return cls.season_url
                        else:
                            return cls.season_url
                i += 1
        except Exception:
            film_link = None
        return film_link

    def parse(self, response, dict_gen, film, url):
        content = simple_tor_get_page(url)
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

        resp_dict = dict_gen(film)

        if film.type == APP_FILM_SERIAL:
            for serial_season in self.serial_list:
                resp_dict['content_type'] = APP_LOCATION_TYPE_ADDITIONAL_MATERIAL_SEASON
                resp_dict['type'] = 'zoomby'
                resp_dict['number'] = serial_season['season']
                resp_dict['value'] = value
                resp_dict['url_view'] = serial_season['season_url']
                resp_dict['price'] = self.get_price()
                resp_list.append(resp_dict)
                for episode in serial_season['episode_list']:
                    resp_dict['content_type'] = APP_LOCATION_TYPE_ADDITIONAL_MATERIAL_EPISODE
                    resp_dict['type'] = 'zoomby'
                    resp_dict['number'] = serial_season['season']
                    resp_dict['value'] = value
                    resp_dict['url_view'] = episode['url']
                    resp_dict['price'] = self.get_price()
                    resp_dict['episode'] = episode['number']
                    resp_list.append(resp_dict)
        else:
            resp_dict['type'] = 'tvigle'
            resp_dict['number'] = 0
            resp_dict['value'] = value
            resp_dict['url_view'] = url
            resp_dict['price'] = self.get_price()
            resp_dict['content_type'] = APP_LOCATION_TYPE_ADDITIONAL_MATERIAL_FILM
            resp_list.append(resp_dict)

        return resp_list

    def get_price(self):
        return 0

    def get_seasons(self):
        return self.serial_list
