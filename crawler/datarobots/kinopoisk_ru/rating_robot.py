# coding: utf-8

import requests
from bs4 import BeautifulSoup

def get_ratings(kinopoisk_id):

    r = requests.get('http://kinopoisk.ru/rating/{}.xml'.format(kinopoisk_id))
    soup = BeautifulSoup(r.content,'xml')

    return {'kp':
            {'votes' : int(soup.rating.kp_rating.attrs['num_vote']),
             'rating' : float(soup.rating.kp_rating.text)
         },
            'imdb':
            {'votes' : int(soup.rating.imdb_rating.attrs['num_vote']),
             'rating' : float(soup.rating.imdb_rating.text)
         }
    }
    


