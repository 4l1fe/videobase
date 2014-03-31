# coding: utf-8
from bs4 import BeautifulSoup


def parse_search(response):
    try:
        films = response.json()['content']
        search_film = films[0]
    except IndexError:
        search_film = None
    return search_film


def parse_film_page(response):
    pass