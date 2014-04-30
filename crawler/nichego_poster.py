# coding: utf-8
from crawler.parse_page import get_image

import requests

HOST = 'nichego.me'


def get_poster(film):
    url = 'http://%s/movies/api/catalog.php' % HOST
    params = dict(
        private='yes',
        offset=0,
        rating=0,
        minvotes_number=0,
        fromyear=0,
        sjanre=-1,
        sname=film.name,
    )
    response = requests.get(url, params=params)
    film_id = response.json()[0]['id']
    template = 'http://%s/movies/api/poster.php?id={}&w=1024' % HOST
    poster = get_image(template, film_id)
    return poster