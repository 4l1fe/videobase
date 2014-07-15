# coding: utf-8
from crawler.core import BaseParse
from bs4 import BeautifulSoup
import re

URL_FILM = ''
SEASONS = [0,]

def parse_search(response, film_name, serial):
    s = u'Сезон'
    mas = []
    reg = re.compile('(?P<season>'+ s +')[ ](?P<number>\d+)')
    try:
        soup = BeautifulSoup(response.content)
        url_seasons = None
        if serial:
            tag_seasons = soup.find('h4')
            a_seasons = tag_seasons.a
            url_seasons = a_seasons.get('href')
            tag_h4 = soup.findAll('h4')
            if tag_h4 is None:
                return None
            for tag in tag_h4:
                tag_a = tag.a
                if tag_a is None:
                    continue
                season_name = tag_a.text
                if film_name in season_name:
                    if u'Сезон' in season_name:
                        search = reg.search(season_name)
                        if int(search.group('number')) in mas:
                            continue
                        mas.append(int(search.group('number')))
            global SEASONS
            SEASONS = mas
            film_link = url_seasons
        if url_seasons is None:
            tag = soup.find('h4', text=film_name)
            tag_a = tag.a
            film_link = tag_a.get('href')

    except:
        film_link = None
    return film_link



class ParseTvigleFilm(object):
    def __init__(self):
        pass
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

    def get_seasons(self):
        global SEASONS
        return SEASONS

    def get_link(self):
        pass



