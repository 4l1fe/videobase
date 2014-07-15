import json

from crawler.tor import simple_tor_get_page

JSON_API = "http://www.kinopoisk.ru/handler_trailer_popup.php"


def get_data_dict(kinopoisk_id):
    content = simple_tor_get_page('http://www.kinopoisk.ru/handler_trailer_popup.php?ids={}'.format(kinopoisk_id))
    return json.loads(content)

    
def update_film_information(film, item):

    assert item['fid'] == film.kinopoisk_id

    film.description = item['desc']

    
    
    
    