# coding: utf-8
from __future__ import absolute_import
from crawler.parse_page import crawler_get


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

import datetime
import  json


information_robots = ['kinopoik_robot', 'imdb_robot']


logger = get_task_logger(__name__)


def get_robot_by_name(robot_name):
    try:
        return Robots.objects.get(robot_name)
    except Robots.DoesNotExist:
        robot = Robots(name=robot_name, description='', delay=1, rstatus=0, state={"id": 1})
        robot.save()
        return robot


def update_robot_state_film_id(robot):

    if robot.state:
        state = robot.state
    else:
        state = '{}'

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


@app.task(name='robot_launch')
def robot_launcher(*args, **kwargs):

    print 'Start'

    for robot in Robots.objects.all():
        print u'Checking robot %s' % robot.name
        print robot.last_start, timezone.now()
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
    Amediatera_robot.get_film_data()

@app.task(name='viaplay_ru_robot_start')
def viaplay_robot_start():
    ViaplayRobot.get_data()


