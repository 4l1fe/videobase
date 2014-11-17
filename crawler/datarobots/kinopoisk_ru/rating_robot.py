# coding: utf-8

import requests
from bs4 import BeautifulSoup


def get_ratings(kinopoisk_id):

    r = requests.get('http://kinopoisk.ru/rating/{}.xml'.format(kinopoisk_id))
    soup = BeautifulSoup(r.content,'xml')
    ratings = {
        'kp': None,
        'imdb': None
    }
    if soup.rating.kp_rating:
        kp_dict = {
                'votes': 0,
                'rating': 0.0
        }
        kp_dict['votes'] = int(soup.rating.kp_rating.attrs['num_vote'])
        kp_dict['rating'] = float(soup.rating.kp_rating.text)
        ratings['kp'] = kp_dict

    if soup.rating.imdb_rating:
        imdb_dict = {
                'votes': 0,
                'rating': 0.0
        }
        imdb_dict['votes'] = int(soup.rating.imdb_rating.attrs['num_vote'])
        imdb_dict['rating'] = float(soup.rating.imdb_rating.text)
        ratings['imdb'] = imdb_dict

    return ratings
    


