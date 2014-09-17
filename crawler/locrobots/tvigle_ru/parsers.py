# coding: utf-8
import string
from bs4 import BeautifulSoup
import re


class ParseTvigleFilm(object):
    def __init__(self):
        pass

    @classmethod
    def parse_search(cls, response, film_name, serial):
        cls.url_film = 'http://www.tvigle.ru'
        cls.seasons = [0, ]
        s = u'Сезон'
        film_link = ''
        film_name = film_name.lower().strip().encode('utf-8').translate(None, string.punctuation)
        reg = re.compile('(?P<season>'+s+')[ ](?P<number>\d+)')
        try:
            soup = BeautifulSoup(response)
            url_seasons = None
            if serial:
                tag_seasons = soup.findAll('a', attrs={'class': 'search-content-title'})
                for tag in tag_seasons:
                    if film_name in tag.text.lower().strip().encode('utf-8').translate(None, string.punctuation):
                        if len(cls.seasons) == 0:
                            cls.seasons.append(1)
                        url_seasons = tag.get('href')
                        season_name = tag.text.lower().strip().encode('utf-8').translate(None, string.punctuation)
                        if 'сезон' in season_name:
                            search = reg.search(season_name)
                            if int(search.group('number')) in cls.seasons:
                                continue
                            cls.seasons.append(int(search.group('number')))

                film_link = cls.url_film + url_seasons
            if url_seasons is None:
                tag_a = soup.findAll('a', attrs={'class': 'search-content-title'})
                for tag in tag_a:
                    if film_name == tag.text.lower().strip().encode('utf-8').translate(None, string.punctuation):
                        link = tag.get('href')
                        film_link = cls.url_film + link
                        return film_link
        except:
            film_link = ''
        return film_link

    def parse(self, response, dict_gen, film, url):
        resp_list = []
        link = url
        price = self.get_price()
        seasons = self.get_seasons()
        try:
            value = url.split('video=')[1]
        except:
            value = ''
        if seasons:
            for season in seasons:
                resp_dict = dict_gen(film)
                resp_dict['type'] = 'tvigle'
                resp_dict['number'] = season
                resp_dict['value'] = value
                resp_dict['url_view'] = link
                resp_dict['price'] = price
                resp_list.append(resp_dict)

        return resp_list

    def get_price(self):
        return 0

    @classmethod
    def get_seasons(cls):
        return cls.seasons

    def get_link(self):
        pass



