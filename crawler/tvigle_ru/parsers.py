# coding: utf-8
from ..core import BaseParse
from bs4 import BeautifulSoup
import re

URL_FILM = ''


def parse_search(response, filmName):
    s = u'Сезон'
    mas = []
    reg = re.compile('(?P<season>'+ s +')[ ](?P<number>\d+)')
    try:
        soup = BeautifulSoup(response.content)
        tag_h4 = soup.findAll('h4')
        if(tag_h4 == None):
            return None
        for tag in tag_h4:
            tagA = tag.a
            if tagA == None:
                continue
            seasonName = tagA.text
            if filmName in seasonName:
                if u'Сезон' in seasonName:
                    search = reg.search(seasonName)
                    if int(search.group('number')) in mas:
                        continue
                    mas.append(int(search.group('number')))
                    print mas

        tag = soup.find('h4',text=filmName)
        tagA = tag.a
        filmLink = tagA.get('href')

    except:
        filmLink = None
    return filmLink



class ParseTvigleFilm(object):
    def __init__(self):
        pass
    def parse(self, response, dict_gen, film,url):
        d = dict_gen(film)
        d['url_view'] = url
        d['price_type'] = 0
        d['price'] = self.get_price()
        return  [d]

    def get_price(self):
        return 0

    def get_seasons(self):
        return [0.]

    def get_link(self):
        pass



