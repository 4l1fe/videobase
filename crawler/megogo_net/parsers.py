from ..core import BaseParse
from bs4 import BeautifulSoup
from apps.contents.constants import *
import re
import json
REGEXP = '(?P<name>.+)[ ][(](?P<year>[0-9]{4}[)])'
def parse_search(response, film):

    try:
        print response.content
        films = json.loads(response.content)
        for film in films:
            print film['title']+'\n'
    except IndexError:
        search_film = None
    return search_film

class ParseMegogoFilm(BaseParse):
    def __init__(self, html):
        super(ParseMegogoFilm, self).__init__(html)
        self.soup = BeautifulSoup(html, "html")

    def get_link(self, **kwargs):
        a =  self.soup
        return 'http://www.megogo.net/ru/'
    def get_price(self, **kwargs):
        price = 0
        price_type = APP_CONTENTS_PRICE_TYPE_FREE
        return price, price_type

    def get_seasons(self, **kwargs):
        return [0]

