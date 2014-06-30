import requests
from apps.films import Films
JSON_API = "http://www.kinopoisk.ru/handler_trailer_popup.php"
from crawler.core.browser import get_random_weighted_browser_string
import json
from django.utils import timezone


def form_candidates():
    pass

def get_data_dict(kinopoisk_id):
    r = requests.get('http://www.kinopoisk.ru/handler_trailer_popup.php',params = {'ids':kinopoisk_id}, headers ={'User-Agent': get_random_weighted_browser_string()})

    return json.loads(r.content)


    
def update_film_information(film,item):

    assert item['fid'] == film.kinopoisk_id

    film.description = item['desc']

    film.kinopoisk_last_try = 
    
    
    