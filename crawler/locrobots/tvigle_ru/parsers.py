# coding: utf-8
import copy
import string
from bs4 import BeautifulSoup
import re
from apps.contents.constants import APP_LOCATION_TYPE_ADDITIONAL_MATERIAL_SEASON, \
    APP_LOCATION_TYPE_ADDITIONAL_MATERIAL_EPISODE, APP_LOCATION_TYPE_ADDITIONAL_MATERIAL_FILM
from apps.films.constants import APP_FILM_SERIAL


class ParseTvigleFilm(object):
    def __init__(self):
        pass

    @classmethod
    def parse_search(cls, response, film_name, serial, load_function):
        cls.url_film = 'http://www.tvigle.ru'
        cls.seasons = [0, ]
        cls.list_url = []
        film_link = ''
        film_name = film_name.lower().strip().encode('utf-8').translate(None, string.punctuation)
        cls.serial_list = []
        season_list = {
            'season': '',
            'season_url': '',
            'episode_list': []
        }
        episode_dict = {
            'number': '',
            'url': ''
        }
        try:
            soup = BeautifulSoup(response)
            if serial:
                cls.seasons = []
                tag_a = soup.findAll('div', {'class': 'category-filter-content left auto-upload'})[0].findAll('a')
                for a in tag_a:
                    if film_name in a.text.lower().strip().encode('utf-8').translate(None, string.punctuation):
                        link = a.get('href')
                        serial_url = cls.url_film + link
                        response = load_function(serial_url)
                        soup = BeautifulSoup(response)

                        try:
                            tag_season = soup.find('div', {'class': 'category-filter-menu left'}).findAll('li')
                        except Exception:
                            season_list['season_url'] = serial_url
                            season_list['season'] = 1
                            season_list['episode_list'].append(episode_dict)
                            cls.list_url.append(season_list)
                            return serial_url

                        for tag_li in tag_season:
                            season_list['episode_list'] = []
                            link = tag_li.a.get('href')
                            season_list['season_url'] = cls.url_film + link
                            season_list['season'] = int(tag_li.a.text.split()[1])
                            response = load_function(season_list['season_url'])
                            soup = BeautifulSoup(response)

                            tags_a = soup.find('div', {'class': 'category-filter-content left'}).findAll('a')

                            for tag_a in tags_a:
                                text = tag_a.text
                                if u'Серия' in text:
                                    if episode_dict['url'] != cls.url_film + tag_a.get('href'):
                                        episode_dict['number'] = int(text.split(u'Серия')[1])
                                        episode_dict['url'] = cls.url_film + tag_a.get('href')
                                        season_list['episode_list'].append(copy.deepcopy(episode_dict))
                            cls.list_url.append(copy.deepcopy(season_list))
                        return cls.url_film + link

            else:
                tag_a = soup.findAll('a', attrs={'class': 'search-content-title'})
                for tag in tag_a:
                    if film_name == tag.text.lower().strip().encode('utf-8').translate(None, string.punctuation):
                        link = tag.get('href')
                        film_link = cls.url_film + link
                        cls.list_url.append(film_link)
                        return film_link
        except:
            film_link = ''
        return film_link

    def parse(self, response, dict_gen, film, url):
        resp_list = []
        try:
            value = url.split('video=')[1]
        except:
            value = ''

        resp_dict = dict_gen(film)

        if film.type == APP_FILM_SERIAL:
            for serial_season in self.list_url:
                resp_dict['content_type'] = APP_LOCATION_TYPE_ADDITIONAL_MATERIAL_SEASON
                resp_dict['type'] = 'tvigle'
                resp_dict['number'] = serial_season['season']
                resp_dict['value'] = value
                resp_dict['url_view'] = serial_season['season_url']
                resp_dict['price'] = self.get_price()
                resp_list.append(resp_dict)
                for episode in serial_season['episode_list']:
                    resp_dict['content_type'] = APP_LOCATION_TYPE_ADDITIONAL_MATERIAL_EPISODE
                    resp_dict['type'] = 'tvigle'
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

    @classmethod
    def get_seasons(cls):
        return cls.seasons

    def get_link(self):
        return self.list_url



