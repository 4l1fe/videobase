# coding: utf-8
from apps.contents.constants import APP_CONTENTS_PRICE_TYPE_PAY
from bs4 import BeautifulSoup


def parse_source(source, film_name, hosts):
    try:
        soup = BeautifulSoup(source)
        tag = soup.find('div', attrs={'class': 'exact-matching'})
        text_h = tag.h1.text
        if film_name in text_h:
            tag_a = tag.a
            ref = tag_a.get('href')
        film_link = hosts + ref
    except:
        film_link = ''
    return film_link


class ParseTvzavrFilmPage(object):
    def __init__(self):
        pass

    def parse(self, response, dict_gen, film, url):
        resp_list = []
        link = url
        price = self.get_price()
        seasons = self.get_seasons()
        if seasons:
            for season in seasons:
                resp_dict = dict_gen(film)
                resp_dict['number'] = season
                resp_dict['url_view'] = link
                resp_dict['price'] = price
                resp_dict['price_type'] = APP_CONTENTS_PRICE_TYPE_PAY
                resp_dict['type'] = 'tvzavr'
                resp_list.append(resp_dict)

        return resp_list

    def get_price(self):
        return 79

    def get_seasons(self):
        return [0, ]

    def get_link(self):
        return ''