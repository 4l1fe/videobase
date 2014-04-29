from apps.films.models import Films
from bs4 import BeautifulSoup
from crawler.robot_start import save_location, sane_dict
import requests


class ViaplayRobot(object):
    def __init__(self):
        pass

    def get_data(self):
        all_film_url = 'http://viaplay.ru/filmy/vse/5/alphabetical'
        response = requests.get(all_film_url)
        content = response.content
        soup_films = BeautifulSoup(content).find('ul', {'class': 'atoz-list'}).li.ul.find_all('li')
        films = Films.objects.all()
        for li_film in soup_films:
            for film in films:
                if li_film.a.text == film.name:
                    link = li_film.a.get('href')
                    d = self.film_dict(film, link)
                    save_location(**d)
                    continue

    def film_dict(self, film, film_link):
        resp_dict = sane_dict(film)
        resp_dict['url_view'] = film_link
        resp_dict['price'] = 0
        return resp_dict