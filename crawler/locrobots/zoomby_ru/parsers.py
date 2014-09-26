# coding: utf-8
import re
from apps.films.constants import APP_FILM_FULL_FILM, APP_FILM_SERIAL
from bs4 import BeautifulSoup
from crawler.tor import simple_tor_get_page

HOST = 'http://www.zoomby.ru'


def parse_search(response, film_name, year):
    try:
        soup = BeautifulSoup(response)
        tag = soup.find(attrs={'class': 'element_row_3'}, text=film_name)
        par_div = tag.parent
        year_tag = par_div.find_all('div', {'class': 'element_row_5'})
        for tag_sp in year_tag:
            tag_span = tag_sp.find('span')
            if tag_span:
                break
                
        year_text = tag_span.text
        film_year = re.search(ur'\d+', year_text).group()
        if year != int(film_year):
            return ''
        tag_a = tag.a
        film_link = tag_a.get('href')
    except:
        film_link = ''
    return film_link


class ParseFilm(object):
    def __init__(self):
        self.parse_value = 'http://www.zoomby.ru/v/'

    def parse(self, response, dict_gen, film, url):
        d = dict_gen(film)
        content = simple_tor_get_page(url)
        value = ''
        isFilm = False
        try:
            soup = BeautifulSoup(content)
            tag = soup.find('meta', attrs={'property': 'og:type'})
            if (not tag is None and film.type == APP_FILM_FULL_FILM)\
                    or (film.type == APP_FILM_SERIAL and tag is None):
                tag = soup.find('div', attrs={'class': 'big_rating'})
                id = tag.get('id')
                value = self.parse_value + id
                isFilm = True
        except:
            pass

        if isFilm:
            d['url_view'] = url
            d['value'] = value
            d['price_type'] = 0
            d['price'] = self.get_price()
            d['type'] = 'zoomby'
            return [d]

        return []

    def get_price(self):
        return 0

    def get_seasons(self):
        return [0, ]
