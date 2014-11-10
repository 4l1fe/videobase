# coding: utf-8
import copy
import string
from bs4 import BeautifulSoup
import re
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
        season_url = {
            'season': '',
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
                            season_url['url'] = serial_url
                            season_url['season'] = 1
                            cls.list_url.append(season_url)
                            cls.seasons.append(1)
                            return serial_url

                        for tag_li in tag_season:
                            link = tag_li.a.get('href')
                            season_url['url'] = cls.url_film + link
                            season_url['season'] = int(tag_li.a.text.split()[1])
                            cls.list_url.append(copy.deepcopy(season_url))
                            cls.seasons.append(int(season_url['season']))
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
        links = self.get_link()

        price = self.get_price()
        seasons = self.get_seasons()
        seasons.sort()

        try:
            value = url.split('video=')[1]
        except:
            value = ''

        if film.type == APP_FILM_SERIAL:
            for season in self.list_url:
                resp_dict = dict_gen(film)
                resp_dict['type'] = 'tvigle'
                resp_dict['number'] = season['season']
                resp_dict['value'] = value
                resp_dict['url_view'] = season['url']
                resp_dict['price'] = price
                resp_list.append(resp_dict)
        else:
            resp_dict = dict_gen(film)
            resp_dict['type'] = 'tvigle'
            resp_dict['number'] = 0
            resp_dict['value'] = value
            resp_dict['url_view'] = links[0]
            resp_dict['price'] = price
            resp_list.append(resp_dict)

        return resp_list

    def get_price(self):
        return 0

    @classmethod
    def get_seasons(cls):
        return cls.seasons

    def get_link(self):
        return self.list_url



