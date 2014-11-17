# coding: utf-8

import requests
from bs4 import BeautifulSoup


def get_ratings(kinopoisk_id):

    r = requests.get('http://kinopoisk.ru/rating/{}.xml'.format(kinopoisk_id))
    soup = BeautifulSoup(r.content,'xml')
    ratings = {
        'kp':
            {
                'votes': 0,
                'rating': 0.0
            },
        'imdb':
            {
                'votes': 0,
                'rating': 0.0
            }
    }
    if soup.rating.kp_rating:
        ratings['kp']['votes'] = int(soup.rating.kp_rating.attrs['num_vote'])
        ratings['kp']['rating'] = float(soup.rating.kp_rating.text)

    if soup.rating.imdb_rating:
        ratings['imdb']['votes'] = int(soup.rating.imdb_rating.attrs['num_vote'])
        ratings['imdb']['rating'] = float(soup.rating.imdb_rating.text)

    return ratings
    


