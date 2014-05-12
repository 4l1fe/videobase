# coding: utf-8
from bs4 import BeautifulSoup
import requests

HOST = 'http://www.zoomby.ru'


def parse_search(response, film_name):
    try:
        soup = BeautifulSoup(response.content)
        tag = soup.find(attrs={'class': 'element_row_3'}, text=film_name)
        tag_a = tag.a
        film_link = tag_a.get('href')
    except:
        film_link = None
    return film_link


class ParseFilm(object):
    def __init__(self):
        self.parse_value = 'http://www.zoomby.ru/v/'

    def parse(self, response, dict_gen, film, url):
        d = dict_gen(film)
        response = requests.get(url)
        soup = BeautifulSoup(response.content)
        tag = soup.find('meta', attrs={'property': 'og:video'})
        d['url_view'] = url
        d['value'] = tag.get('content').replace(self.parse_value, '')
        d['price_type'] = 0
        d['price'] = self.get_price()
        return [d]

    def get_price(self):
        return 0

    def get_seasons(self):
        return [0, ]
