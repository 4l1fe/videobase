# coding: utf-8
from ..core import BaseParse

from bs4 import BeautifulSoup
HOST = 'http://www.now.ru'
FILM_URL = ''
COST = 0
# Парсер для поисковика фильма
def parse_search(response, film):
    searchTextTitle = 'Результаты поиска'.decode('utf-8')
    filmDiv = None
    exitFlag = False
    try:
        content = response.content
        soup = BeautifulSoup(content)
        if(soup.select('div.noresults')!= None):
            return None
        if(searchTextTitle in soup.head.title.text):
            for tag in soup.select('div.play-about'):
                if(exitFlag):
                    break
                for h2 in tag.find_all('h2'):
                    h2.span.extract()
                    if(h2.text.lower().strip() == film.decode('utf-8').lower().strip()):
                        filmDiv = h2.parent.parent.parent
                        exitFlag = True
                        break
            if(filmDiv != None):
                aTag = filmDiv.a
                costDiv = filmDiv.find(attrs={'class':'watch_container'})
                if(costDiv != None):
                    global COST
                    COST = costDiv.span.getText().strip().split(' ')[0]
                filmLink = HOST + aTag.get('href')
        else:
            filmLink = soup.find(attrs={'property':'og:url'}).get('content')

        global FILM_URL
        FILM_URL = filmLink

    except IndexError:
        filmLink = None
    return filmLink

# Парсер для страници фильма
class ParseNowFilmPage(object):
    def parse(self, response, dict_gen, film, url):
        d = dict_gen(film)
        d['url_view'] = url
        d['price_type'] = 0
        d['price'] = self.get_price()
        return  [d]
    def get_price(self):
       return COST

    def get_seasons(self):
        [0,]

    def get_link(self):
       pass