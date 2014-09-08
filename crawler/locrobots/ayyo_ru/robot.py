# coding: utf-8
import json
import urllib
from crawler.locations_saver import save_location_to_locs_dict

HOST = 'www.ayyo.ru'
URL_SEARCH = 'api/search/live/?{}'
from apps.films.models import Films
from crawler.utils.locations_utils import save_location, sane_dict
from crawler.tor import simple_tor_get_page
from apps.contents.constants import *
import string


class AyyoRobot(object):
    def __init__(self, film_id):
        self.film = Films.objects.get(id=film_id)
        search_film = urllib.urlencode({'text': (self.film.name.encode('utf-8'))})
        search_url = URL_SEARCH.format(search_film)
        url = "https://%s/%s" % (HOST, search_url, )
        self.response = simple_tor_get_page(url)

    def get_data(self):
        locations = []
        site_name = 'www.ayyo.ru'
        try:
            films = json.loads(self.response)['live_search']['search_movies_result']
            for film in films:
                if film['rus_title'].lower().strip().encode('utf-8').translate(None, string.punctuation) == self.film.name.lower().strip().encode('utf-8').translate(None, string.punctuation):
                    film_link = 'https://www.ayyo.ru/movies/%s/' % (film['slug'])
                    ayyo_film_id = film['movie']
                    break
            film_url = 'https://www.ayyo.ru/api/movies/?{}'.format(urllib.urlencode({'id__in': ayyo_film_id}))
            film_response = simple_tor_get_page(film_url)
            price = float(json.loads(film_response)['movies']['data'][str(ayyo_film_id)]['streaming_price'])
            d = self.film_dict(self.film, film_link, price)
            save_location(**d)
            save_location_to_locs_dict(locations, **d)
        except Exception, e:
            pass
        return site_name, locations

    def film_dict(self, film, film_link, price):
        if price == 0:
            price_type = APP_CONTENTS_PRICE_TYPE_FREE
        else:
            price_type = APP_CONTENTS_PRICE_TYPE_PAY
        resp_dict = sane_dict(film)
        resp_dict['number'] = 0
        resp_dict['url_view'] = film_link
        resp_dict['price_type'] = price_type
        resp_dict['price'] = price
        return resp_dict