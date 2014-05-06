# coding: utf-8
from ..core import BaseParse
from apps.contents.constants import *
import re
from bs4 import BeautifulSoup


# Парсер для поисковика фильма
def parse_search(response, film):
    if not (type(film) is unicode):
        film = film.decode('utf-8')

    HOST = 'http://www.now.ru'
    search_text_title = 'Результаты поиска'.decode('utf-8')
    film_div = None
    exit_flag = False
    try:
        content = response.content
        soup = BeautifulSoup(content)
        if not(soup.find(attrs={'id': 'noresults'}) is None):
            return None
        if search_text_title in soup.head.title.text:
            for tag in soup.select('div.play-about'):
                if exit_flag:
                    break
                for h2 in tag.find_all('h2'):
                    h2.span.extract()
                    if h2.text.lower().strip() == film.lower().strip():
                        film_div = h2.parent.parent.parent
                        exit_flag = True
                        break
            if film_div:
                a_tag = film_div.a
                film_link = HOST + a_tag.get('href')
            else:
                return None
        else:
            film_link = soup.find(attrs={'property':'og:url'}).get('content')

    except IndexError:
        film_link = None
    return film_link


# Парсер для страници фильма
class ParseNowFilmPage(BaseParse):
    def __init__(self, html):
        super(ParseNowFilmPage, self).__init__(html)
        self.soup = BeautifulSoup(html, "html")

    def get_link(self, **kwargs):
        link = self.soup.find(attrs={'property': 'og:url'}).get('content')
        return link

    def get_price(self, **kwargs):
        price = 0
        price_type = APP_CONTENTS_PRICE_TYPE_FREE
        root_div = self.soup.find('div', {'class': ['content-prices', 'bookmarked']})
        div_price = root_div.find('div', {'class': 'watch_additional_container'})
        if div_price is not None:
            price_type = APP_CONTENTS_PRICE_TYPE_PAY
            price = float(div_price.span.getText().strip().split(' ')[0])
        else:
            div_price = root_div.find('div', {'class': 'watch_container'})
            if div_price is not None:
                reg = re.search(ur'\d+', div_price.span.text)
                if div_price.input['value'] == u'Подписка':
                    price_type = APP_CONTENTS_PRICE_TYPE_SUBSCRIPTION
                    price = float(reg.group())
                elif reg is not None:
                    price_type = APP_CONTENTS_PRICE_TYPE_PAY
                    price = float(reg.group())
        return price, price_type

    def get_seasons(self, **kwargs):
        seasons_div = self.soup.find('div', {'class': 'balloontabs'})
        if seasons_div is not None:
            seasons = seasons_div.find_all('div', {'class': 'balloontab'})
            return range(1, len(seasons)+1)
        else:
            return [0]