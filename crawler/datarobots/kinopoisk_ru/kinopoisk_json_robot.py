# coding: utf-8

import json
from crawler.tor import simple_tor_get_page

JSON_API = "http://www.kinopoisk.ru/handler_trailer_popup.php"


def get_data_dict(kinopoisk_id):
    url = 'http://www.kinopoisk.ru/handler_trailer_popup.php?ids={id}'.format(id=kinopoisk_id)
    content = simple_tor_get_page(url)
    return json.loads(content)


def update_film_information(film, item):
    assert item['fid'] == film.kinopoisk_id
    film.description = item['desc']
