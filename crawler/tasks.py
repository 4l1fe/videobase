# coding: utf-8

from __future__ import absolute_import
from apps.films.models import Persons
from bs4 import BeautifulSoup
from crawler.core import simple_get
from crawler.parse_page import crawler_get, get_photo
from django.core.files import File
from django.db import transaction

from django.utils import timezone

from celery import shared_task
from celery.utils.log import get_task_logger
import requests

from videobase.celery import app
from crawler.robot_start import sites_crawler, launch_next_robot_try_for_kinopoisk, process_film_on_site
from apps.robots.models import Robots
from crawler.kinopoisk_poster import poster_robot_wrapper
from crawler.imdbratings import process_all
from crawler.amediateka_ru.loader import Amediateka_robot
from crawler.viaplay_ru.robot import ViaplayRobot
from crawler.kinopoisk_premiere import kinopoisk_news
from crawler.youtube_trailers import process_film
from apps.films.models import Films
from crawler.playfamily_xml import process
from crawler.task_modules.kinopoisk_one_page import kinopoisk_parse_one_film


import datetime
import  json
from functools import partial

KINOPOISK_LIST_FILMS_URL = "http://www.kinopoisk.ru/top/navigator/m_act%5Begenre%5D/999/m_act%5Bnum_vote%5D/10/m_act%5Brating%5D/1:/m_act%5Bis_film%5D/on/m_act%5Bis_mult%5D/on/order/year/page/{}/#results"
information_robots = ['kinopoik_robot', 'imdb_robot']


logger = get_task_logger(__name__)

def get_robot_by_name(robot_name):
    try:
        return Robots.objects.get(name=robot_name)
    except Robots.DoesNotExist:
        robot = Robots(name=robot_name, last_start=timezone.now() , description=' ', delay=1, rstatus=0, state={"id": 1})
        robot.save()
        return robot


def update_robot_state_film_id(robot):

    if robot.state:
        state = robot.state
    else:
        state = '{}'
    if type(state) is dict:
        pstate = state
    else:
        try:
            pstate =json.loads(state)
        except ValueError:
            pstate ={}
    if 'id' in pstate:
        film_id = pstate['id']
        pstate['id'] +=1
    else:
        pstate['id'] =1
        film_id =1


    robot.state = json.dumps(pstate)

    robot.last_start = timezone.now()
    robot.save()

    return film_id

def robot_launch_wrapper(robot_name,func):
        robot = get_robot_by_name(robot_name)
        item_id =update_robot_state_film_id(robot)
        print "Starting robot {} for id = {}".format(robot_name,item_id)
        func(item_id)

def robot_task(robot_name):
    def decor(func):
        @app.task(name=robot_name)
        def wrapper():
            robot_launch_wrapper(robot_name,func)
        return wrapper
    return decor

@app.task(name='kinopoisk_films')
def kinopoisk_films(page):
    count = page
    try:
        if page == 11:
            data = BeautifulSoup(simple_get(KINOPOISK_LIST_FILMS_URL.format(1)).content)
            pages = data.find('div', attrs={'class': 'pagesFromTo'})
            count = int(pages.text.split(' ')[2])

        for i in range(1, count+1):
            print count
            data = BeautifulSoup(simple_get(KINOPOISK_LIST_FILMS_URL.format(i)).content)
            list_films = data.findAll('div', attrs={'class': 'name'})
            print("!!!!!!!!"+str(i))
            for film in list_films:
                name = film.a.text
                kinopoisk_id = int(film.a.get('href').split('/')[4])
                if u'(сериал)' in name:
                    name = name.replace(u'(сериал)', '')
                try:
                    Films.objects.get(kinopoisk_id=kinopoisk_id)
                except Films.DoesNotExist:
                    film = Films()
                    film.name = name
                    film.kinopoisk_id = kinopoisk_id
                    film.type = ''
                    film.save()
    except Exception, e:
        print e


@robot_task('kinopoisk_persons')
def parse_kinopoisk_persons(id):
        try:
            response = crawler_get('http://www.kinopoisk.ru/name/{}/view_info/ok/#trivia'.format(id))
            soup = BeautifulSoup(response.content)
            tag = soup.find('span', attrs={'itemprop': 'alternativeHeadline'})
            person_name = tag.text.strip()
            p = Persons.objects.get(name=person_name)
            tag_birthdate = soup.find('td', attrs={'class': 'birth'})
            birthdate = ''
            if not (tag_birthdate is None):
                birthdate = tag_birthdate.get('birthdate')
            else:
                print 'No data birthdate for this person id = %s' % id
            tags_bio = soup.findAll('li', attrs={'class': 'trivia'})
            bio = ''
            if len(tags_bio):
                for li in tags_bio:
                    bio = bio + ' ' + li.text
            else:
                print 'No biography for this person id = %s' % id
            p.birthdate = birthdate
            p.bio = bio
            p.kinopoisk_id = id
            if p.photo == '' and p.kinopoisk_id != 0:
                p.photo.save('profile.jpg', File(get_photo(p.kinopoisk_id)))
            p.save()
        except Exception, e:
            print e

@app.task(name='individual_site_film')
def launch_individual_film_site_task(site):

    robot_launch_wrapper(site,
                         partial(process_film_on_site,site))


@app.task(name='robot_launch')
def robot_launcher(*args, **kwargs):

    print 'Start'

    for robot in Robots.objects.all():
        print u'Checking robot %s' % robot.name
        if robot.last_start + datetime.timedelta(seconds=robot.delay) < timezone.now():

            if robot.name in sites_crawler:
                launch_individual_film_site_task.apply_async((robot.name,))
        else:
            print u'Skipping robot %s' % robot.name


@app.task(name='kinopoisk_get_id')
def kinopoisk_get_id(*args, **kwargs):
    print 'Start'
    robot = Robots.objects.get(name='kinopoisk_get_id')
    print u'Checking robot %s' % robot.name
    print robot.last_start, timezone.now()
    if robot.last_start + datetime.timedelta(seconds=robot.delay) < timezone.now():
            launch_next_robot_try_for_kinopoisk(robot)
    else:
        print u'Skipping robot %s' % robot.name

@app.task(name='kinopoisk_set_poster')
def kinopoisk_set_paster(*args,**kwargs):
    print "Start robot for setting posters"
    robot = Robots.objects.get(name='kinopoisk_set_poster')

    if robot.last_start + datetime.timedelta(seconds=robot.delay) < timezone.now():
        film_id = update_robot_state_film_id(robot)
        poster_robot_wrapper(film_id)

    else:
        print u'Skipping robot %s' % robot.name

@app.task(name='imdb_rating_update')
def imdb_robot_start(*args,**kwargs):
    process_all()


@app.task(name='amediateka_ru_robot_start')
def amediateka_robot_start(*args,**kwargs):
    Amediateka_robot().get_film_data()

@app.task(name='viaplay_ru_robot_start')
def viaplay_robot_start():
    ViaplayRobot().get_data()



def compare_time(film,years):
    '''
    Returns true if @film less than @years old
    '''
    return timezone.now().date() - film.release_date < timezone.timedelta(days = 365*years)

def kinopoisk_compare_time(film,days):
    '''
    Returns true if @film last checked on kinopoisk more than  @days ago
    '''
    if film.kinopoisk_lastupdate:
        return timezone.now() - film.kinopoisk_lastupdate > timezone.timedelta(days = days)
    else:
        return True
 

@app.task(name = 'kinopoisk_refresher')
def create_due_refresh_tasks():

    for film in Films.objects.all():

        if compare_time(film, years=2):
            if kinopoisk_compare_time(film, days=7):
                kinopoisk_parse_one_film.apply_async((film.kinopoisk_id, film.name))
        elif compare_time(film, years=4):
            if kinopoisk_compare_time(film, days=30):
                kinopoisk_parse_one_film.apply_async((film.kinopoisk_id, film.name))
        else:
            if kinopoisk_compare_time(film, days=180):
                kinopoisk_parse_one_film.apply_async((film.kinopoisk_id, film.name))

@app.task(name = 'playfamily_xml')
def pltask():
    process()

@app.task(name= 'kinopoisk_news')
def parse_kinopoisk_news():
    '''
    Periodic task for parsing new films from kinopoisk

    For each film found on premiere page, parser called asynchronously
    '''
    for name,kinopoisk_id in kinopoisk_news():
        kinopoisk_parse_one_film.apply_async((kinopoisk_id,name))

@app.task(name="find_trailer_for_film")
def find_trailer(film_id):

    film = Films.objects.get(id =film_id)
    process_film(film)

@app.task(name = 'youtube_trailers_all')
def trailer_commands():
    for film in Films.objects.all():
        find_trailer.apply_async((film.id,))
        


