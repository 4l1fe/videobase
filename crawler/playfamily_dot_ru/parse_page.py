# coding: utf-8
'''
Module responsible for parsing one page from playfamily.ru
'''


import microdata
from bs4 import BeautifulSoup
import logging
from crawler.playfamily_dot_ru.utils import rub_to_int, utfdecode


def extract_price(soup):
    '''
    Given BeautifuSoup object from page
    from
    http://playfamily.ru
    return price in rubles as int

    '''
    price_tag = [tag for tag in soup.select('a.js-link')
                 if ('title' in tag.attrs)
                 and (u'Смотреть' == tag.attrs['title'])
                 and len(tag.select('span'))][0]

    span = price_tag.select('span')[0]
    span.extract()
    price_rub = rub_to_int(price_tag.text)
    return price_rub


def form_url_from_name(name_orig):

    '''
    If original name of the movie contains only english characters
    then return link
    that probably holds information about this movie.

    i.e 'The Matrix' -> 'http://playfamily.ru/the-matrix'

    '''
    try:
        nul = name_orig.strip().decode('ascii').lower()
        return 'http://playfamily.ru/' + nul.replace(' ', '-')
    except UnicodeDecodeError:
        return None

@utfdecode
def parse_page(page_dump):
    '''
    Parse page
    '''

    item = [i for i in  microdata.get_items(page_dump) if 'name' in i.props][0]
    print item.name.strip()
    print item.alternativeHeadline.strip()

    try:
        soup = BeautifulSoup(page_dump)
        price = extract_price(soup)
    except:
        logging.debug("Can't extract price for %s'", item.name.strip())
        price = None
    return (price, item.name.strip(), item.alternativeHeadline.strip())


DEBUG = __name__ == "__main__"

if DEBUG:
    with open('/home/denis/crawler/l.html') as fr:
        DATA = fr.read()
        print parse_page(DATA)

