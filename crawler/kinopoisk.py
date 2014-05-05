# coding: utf-8
import requests
import time
import random
import re

from bs4 import BeautifulSoup

from .core.browser import simple_get

KINOPOISK = 'www.kinopoisk.ru'


def get_link_from_html(html):
    soup = BeautifulSoup(html)
    return soup.find('div', {'class': ['most_wanted']}).\
        find('div', {'class': 'info'}).find('a')['href']


def get_id_by_film(film, load_function=simple_get):
    url = "http://%s/%s" % (KINOPOISK, 'index.php')
    time.sleep(random.randint(1, 16))
    response = load_function(url, params={'first': 'no', 'what': '',
                                         'kp_query': film.name})
    href = get_link_from_html(response.text)
    id = int(re.findall('/film/(\d+)', href)[0])
    return id
