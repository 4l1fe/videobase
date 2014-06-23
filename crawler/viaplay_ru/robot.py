
from apps.films.models import Films
from bs4 import BeautifulSoup
from crawler.locations_utils import save_location, sane_dict
from apps.contents.constants import *
import requests


class ViaplayRobot(object):
    def __init__(self):
        self.price = float(395)
        self.price_type = APP_CONTENTS_PRICE_TYPE_SUBSCRIPTION

    def get_data(self):
        all_film_url = 'http://viaplay.ru/filmy/vse/5/alphabetical'
        response = requests.get(all_film_url)
        content = response.content
        soup_films = BeautifulSoup(content).find('ul', {'class': 'atoz-list'}).li.ul.find_all('li')
        films = Films.objects.values('name', 'id')
        for li_film in soup_films:
            for film in films:
                if li_film.a.text == film['name']:
                    link = 'http://viaplay.ru' + li_film.a.get('href')
                    film_query_set = Films.objects.filter(id=film['id'])
                    for obj in film_query_set:
                        d = self.film_dict(obj, link)
                        save_location(**d)
                    break

    def film_dict(self, film, film_link):
        resp_dict = sane_dict(film)
        resp_dict['url_view'] = film_link
        resp_dict['price_type'] = self.price_type
        resp_dict['price'] = self.price
        resp_dict['type'] = 'viaplay'
        return resp_dict