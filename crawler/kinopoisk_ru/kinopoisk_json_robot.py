from apps.films.models import Films
JSON_API = "http://www.kinopoisk.ru/handler_trailer_popup.php"
import json
from django.utils import timezone
from crawler.tor import simple_tor_get_page


def form_candidates():
    pass

def get_data_dict(kinopoisk_id):
    
    content = simple_tor_get_page('http://www.kinopoisk.ru/handler_trailer_popup.php?ids={}'.format(kinnopoisk_id))
    return json.loads(content)


    
def update_film_information(film,item):

    assert item['fid'] == film.kinopoisk_id

    film.description = item['desc']

    
    
    
    