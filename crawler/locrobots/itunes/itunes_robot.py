from bs4 import BeautifulSoup
from apps.contents.constants import APP_CONTENTS_PRICE_TYPE_PAY
from apps.films.models import Films
from crawler.tor import simple_tor_get_page
from crawler.utils.locations_utils import sane_dict


class ItunesRobot(object):
    def get_film_list(self):
        list_film_link = []
        url = 'http://www.apple.com/ru/itunes/charts/movies/'

        content = simple_tor_get_page(url)
        soup = BeautifulSoup(content)

        tags_li = soup.find('section', {'class': 'section movies grid'}).findAll('li')

        for li in tags_li:
            list_film_link.append(li.a.get('href'))

        return list_film_link

    def film_data(self):
        list_film_link = self.get_film_list()
        for link in list_film_link:
            content = simple_tor_get_page(link)
            a,b,c = self.parse_film_page(content)

            dic = self.get_film_dict(a)

            print dic

    def parse_film_page(self, content):
        soup = BeautifulSoup(content)
        film_name = soup.find('h1').text
        price_text = soup.find('span', {'class': 'price'}).text.split()
        film_price = float(price_text[0])
        price_type = APP_CONTENTS_PRICE_TYPE_PAY
        return film_name, film_price, price_type

    def get_film_dict(self, film_name):
        film_dict = None

        film = Films.objects.get(name=film_name)
        film_dict = sane_dict(film)

        return film_dict




