# coding: utf-8
import urllib
import urllib2
from apps.films.models import Films
from crawler.core.exceptions import NoSuchFilm
from crawler.locrobots.mosfilm_ru.parser import parse_search
from crawler.utils.locations_utils import sane_dict, save_location


URL_LOAD = ''
HOST = 'cinema.mosfilm.ru'


class MosfilmRobot(object):
    def __init__(self, film_id):
        self.film = Films.objects.get(pk=film_id)
        search_film = urllib.urlencode({'sb_search_words': self.film.name.encode('utf-8'), 'p_f_1_title': self.film.name.encode('utf-8'), 'p_f_2_title': self.film.name.encode('utf-8')})
        self.url_search = 'search/?{}'.format(search_film)

    def get_data(self):
        url = "http://%s/%s" % (HOST, self.url_search, )
        content = urllib2.urlopen(url)
        film_link = parse_search(content, self.film.name.encode('utf-8'))
        if film_link is None:
            raise NoSuchFilm(self.film)
        dict_film = self.get_dict(self.film, film_link)
        save_location(**dict_film)

    def get_dict(self, film, film_link):
        link = film_link
        resp_dict = sane_dict(film)
        resp_dict['type'] = 'mosfilm'
        resp_dict['value'] = link
        resp_dict['url_view'] = link
        resp_dict['price'] = 0
        return resp_dict
