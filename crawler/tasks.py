# coding: utf-8
from __future__ import absolute_import
from apps.films.models import Persons
from bs4 import BeautifulSoup
from crawler.parse_page import crawler_get, get_photo
from django.core.files import File
from django.db import transaction

from django.utils import timezone

from celery import shared_task
from celery.utils.log import get_task_logger

from videobase.celery import app
from crawler.robot_start import launch_next_robot_try, sites_crawler, launch_next_robot_try_for_kinopoisk
from apps.robots.models import Robots
from crawler.kinopoisk_poster import  poster_robot_wrapper
from crawler.imdbratings import process_all
from crawler.amediateka_ru.loader import Amediateka_robot
from crawler.viaplay_ru.robot import ViaplayRobot
from crawler.kinopoisk import parse_from_kinopoisk
from crawler.kinopoisk_premiere import kinopoisk_news


import datetime
import  json


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

def robot_task(robot_name):
    def decor(func):
        @app.task(name=robot_name)
        def wrapper():
            robot = get_robot_by_name(robot_name)
            item_id =update_robot_state_film_id(robot)
            print "Starting robot {} for id = {}".format(robot_name,item_id)
            func(item_id)
        return wrapper
    return decor


@robot_task('kinopoisk_poster')
def get_person_poster(person_id):
    try:
        p = Persons.objects.get(id=person_id)
        if p.photo == '' and p.kinopoisk_id != None:
            p.photo.save('profile.jpg', File(get_photo(p.kinopoisk_id)))
    except Robots.DoesNotExist:
        pass


@robot_task('kinopoisk_id_person')
@transaction.commit_on_success
def parse_id_persons(id):
        try:
            response = crawler_get('http://www.kinopoisk.ru/name/' + str(id))
            soup = BeautifulSoup(response.content)
            tag = soup.find('span', attrs={'itemprop': 'alternativeHeadline'})
            person_name = tag.text.strip()
            f = Persons.objects.get(name=person_name)
            f.kinopoisk_id = id
            f.save()
        except Exception:
            pass


@app.task(name='robot_launch')
def robot_launcher(*args, **kwargs):

    print 'Start'

    for robot in Robots.objects.all():
        print u'Checking robot %s' % robot.name
        if robot.last_start + datetime.timedelta(seconds=robot.delay) < timezone.now():

            if robot.name in sites_crawler:
                launch_next_robot_try(site=robot.name)
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


@app.task(name = 'kinopoisk_parse_film_by_id')
def kinopoisk_parse_one_film(kinopoisk_id,name):

    parse_from_kinopoisk(kinopoisk_id=kinopoisk_id, name = name)


@app.task(name= 'kinopoisk_news')
def parse_kinopoisk_news():
    for name,kinopoisk_id in kinopoisk_news():
        kinopoisk_parse_one_film.apply_async((kinopoisk_id,name))
        

        