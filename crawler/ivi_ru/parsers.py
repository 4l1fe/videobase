# coding: utf-8
from ..core import BaseParse

from bs4 import BeautifulSoup


# Парсер для поисковика фильма
def parse_search(response):
    try:
        films = response.json()['content']
        search_film = films[0]
    except IndexError:
        search_film = None
    return search_film


# Парсер для страници фильма
class ParseFilmPage(BaseParse):
    def get_cost(self):
        pass

    def get_series(self):
        pass

    def get_link(self):
        pass
