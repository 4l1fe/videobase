# coding: utf-8
from bs4 import BeautifulSoup

HOST = 'cinema.mosfilm.ru'


def parse_search(content, filmName):
    try:
        soup = BeautifulSoup(content)
        tag = soup.find('a', text=filmName)
        link = tag.get('href')
        film_link = "http://%s%s" % (HOST, link, )
    except:
        film_link = ''
    return film_link



