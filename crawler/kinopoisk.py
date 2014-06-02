# coding: utf-8
import requests
import time
import random
import re
import logging

from bs4 import BeautifulSoup

from .core.browser import simple_get
from apps.films.models import Films, PersonsFilms, Persons, Genres, FilmExtras, Countries
from apps.films.constants import APP_PERSON_PHOTO_DIR,APP_FILM_CRAWLER_LIMIT,APP_FILM_CRAWLER_DELAY,APP_FILM_TYPE_ADDITIONAL_MATERIAL_POSTER, APP_FILM_FULL_FILM
from apps.robots.models import KinopoiskTries
from apps.robots.constants import APP_ROBOT_FAIL, APP_ROBOT_SUCCESS
from crawler.parse_page import acquire_page, parse_one_page
from django.core.files import File
from optparse import make_option
from crawler.kinopoisk_poster import set_kinopoisk_poster
from time import sleep
from django.utils.timezone import now
import logging


KINOPOISK = 'www.kinopoisk.ru'


def get_link_from_html(html):
    soup = BeautifulSoup(html)
    return soup.find('div', {'class': ['most_wanted']}).\
        find('div', {'class': 'info'}).find('a')['href']


def get_id_by_film(film, load_function=simple_get):
    url = "http://%s/%s" % (KINOPOISK, 'index.php')
    time.sleep(random.randint(1, 16))
    response = load_function(url, params={'first': 'no', 'what': '',
                                         'kp_query': film.name})
    href = get_link_from_html(response.text)
    id = int(re.findall('/film/(\d+)', href)[0])
    return id


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

LIMIT = 10


def get_person(name):

    f = Persons.objects.filter(name=name)

    if f:
        return f[0]
    else:
        p = Persons(name=name, photo='')
        p.save()
        print u'Added Person {}'.format(name)
        return p


def get_genre(name):
    g = Genres.objects.filter(name = name)
    if g:
        return g[0]
    else:
        go = Genres(name=name,description = '')
        go.save()
        print u'Added Genre {}'.format(name)
        return go


def get_country(name):
    g = Countries.objects.filter(name= name)
    if g:
        return g[0]
    else:
        go = Countries(name=name, description='')
        go.save()
        print u'Added Country {}'.format(name)
        return go

flatland = get_country(u'Флатландию')


def process_film(film, pdata):
    '''
    
    '''
    a = []

    for d in pdata['Films']:
        a.extend(d.items())
    for key, value in dict(a).items():
        setattr(film, key, value)
    film.kinopoisk_lastupdate = now()
    film.save()
    print u"Updated data for {}".format(film)

    for p in pdata['Persons']:
        try:
            print u"Found person {}".format(p['name'])
            po = get_person(p['name'])
            if 'photo' in p:
                print u"Found foto for {}".format(po)
                if not (po.photo != '' or (p['photo'] is None)):
                    po.photo.save('profile.jpg', File(p['photo']))

            if PersonsFilms.objects.filter(film=film,person=po):
                pass
            else:
                print u"Adding link for film {} and person {}".format(film,po)
                pf = PersonsFilms(person=po, film=film, p_type=p['p_type'])
                pf.save()
        except Exception,e:
            print e
    for g in pdata['Genres']:
        go = get_genre(g['name'])
        if not(go in film.genres.all()):
            print u"Setting {} genre for {}".format(go,film)
            film.genres.add(go)

    for c in pdata['Countries']:
        if flatland in film.countries.all():
            film.countries.remove(flatland)
        co = get_country(c['name'])
        if not(co in film.countries.all()):
            print u"Adding {} country to {} film".format(co,film)
            film.countries.add(co)


    set_kinopoisk_poster(film)

    print u"Saving {} film object".format(film)
    film.save()
def parse_from_kinopoisk(kinopoisk_id,name=None,film = None):
    if film is None:
        try:
            film = Films.objects.get(kinopoisk_id=kinopoisk_id)
        except Films.DoesNotExist:
            print u"Creating new film object with name {} and kinopoisk_id {}".format(name,kinopoisk_id)
            film = Films(kinopoisk_id =kinopoisk_id,
                         name = name if name else u' ',
                         type = APP_FILM_FULL_FILM,
                         release_date =now()
                     )
            film.save()            
    page_dump = u'Failed to acquire page_dump'
    try:
        page_dump = acquire_page(film.kinopoisk_id)
        pdata = parse_one_page(page_dump)
        process_film(film, pdata)
    except Exception, e:
        logging.debug(u"Caught exception : %s", str(e))



