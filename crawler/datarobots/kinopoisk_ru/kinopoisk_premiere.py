# coding: utf-8
from crawler.tor import simple_tor_get_page

from bs4 import BeautifulSoup

KINOPOISK_PREMIERES_URL = "http://www.kinopoisk.ru/premiere"


def kinopoisk_news():
    data = BeautifulSoup(simple_tor_get_page(KINOPOISK_PREMIERES_URL).content.decode('cp1251'))
    
    big_names = data.select('span.name_big')
    names = data.select('span.name')
    
    for name in big_names + names:
        if name.a:
            kinopoisk_id = int(name.a.attrs['href'].split('/')[2])
            kinopoisk_name = name.a.text
            yield kinopoisk_name, kinopoisk_id

if __name__ == "__main__":
    for n in kinopoisk_news():
        print n