# coding: utf-8
import string
from bs4 import BeautifulSoup
from crawler.core.exceptions import NoSuchFilm
from apps.contents.constants import APP_CONTENTS_PRICE_TYPE_SUBSCRIPTION
from apps.films.constants import APP_FILM_FULL_FILM, APP_FILM_SERIAL

HOST = 'http://oll.tv/'


class ParseOllFilm(object):
    def __init__(self):
        self.host = HOST

    def parse(self, response, dict_gen, film, url):
        resp_list = []
        link = self.get_link(response, film)
        if link is None:
            raise NoSuchFilm(film)
        price = self.get_price()
        seasons = self.get_seasons(response, film)
        if seasons:
            for season in seasons:
                resp_dict = dict_gen(film)
                resp_dict['number'] = season
                resp_dict['type'] = 'olltv'
                resp_dict['url_view'] = link
                resp_dict['price'] = price
                resp_dict['price_type'] = APP_CONTENTS_PRICE_TYPE_SUBSCRIPTION
                resp_list.append(resp_dict)

        return resp_list

    def get_link(self, response, film):
        film_name = film.name
        film_link = None
        film_year = film .release_date.year
        try:
            soup = BeautifulSoup(response)
            if film.type == APP_FILM_SERIAL:
                tags_h1 = soup.findAll('h1', attrs={'itemprop': 'name'})
                for h1 in tags_h1:
                    if film_name.lower().strip() in h1.text.lower().strip():
                        tag = soup.find('meta', attrs={'property': 'og:url'})
                        return tag.get('content')
            tags_h1 = soup.findAll('h1', attrs={'itemprop': 'name'})
            tag_year = int(soup.find('strong', attrs={'itemprop': 'copyrightYear'}).text)
            for h1 in tags_h1:
                if h1.text.lower().strip().encode('utf-8').translate(None, string.punctuation) == film_name.lower().strip().encode('utf-8').translate(None, string.punctuation) and tag_year == film_year:
                    tag = soup.find('meta', attrs={'property': 'og:url'})
                    return tag.get('content')
            tags_h3 = soup.findAll('h3')
            for h3 in tags_h3:
                if h3.text.lower().strip() == film_name.lower().strip():
                    tag_a = h3.a
                    link = tag_a.get('href')
                    return self.host + link
        except:
            film_link = None
        return film_link

    def get_price(self):
        return 120

    def get_seasons(self, response, film):
        try:
            mas = [0, ]
            if film.type == APP_FILM_FULL_FILM:
                return mas
            soup = BeautifulSoup(response)
            tag_season = soup.findAll('a', attrs={'class': 'accordion-toggle collapsed'})
            for tag_a in tag_season:
                season_text = tag_a.text
                season = season_text.strip().split(' ')[1]
                if int(season) in mas:
                    continue
                mas.append(int(season))
        except:
            mas = [0, ]
        return mas


