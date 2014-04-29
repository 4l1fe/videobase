# coding: utf-8
from __future__ import absolute_import

from django.utils import timezone

from celery import shared_task
from celery.utils.log import get_task_logger

from videobase.celery import app
from crawler.robot_start import launch_next_robot_try, sites_crawler, launch_next_robot_try_for_kinopoisk, kinopoisk
from apps.robots.models import Robots
from crawler.kinopoisk_poster import  poster_robot_wrapper

import datetime
import logging
import  json


information_robots = ['kinopoik_robot', 'imdb_robot']


logger = get_task_logger(__name__)


@app.task(name='robot_launch')
def robot_launcher(*args, **kwargs):

    print 'Start'

    for robot in Robots.objects.all():
        print u'Checking robot %s' % robot.name
        print robot.last_start, timezone.now()
        if robot.last_start + datetime.timedelta(minutes=robot.delay) < timezone.now():

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
    if robot.last_start + datetime.timedelta(minutes=robot.delay) < timezone.now():
            launch_next_robot_try_for_kinopoisk(robot)
    else:
        print u'Skipping robot %s' % robot.name

@app.task(name='kinopoisk_set_poster')
def kinopoisk_set_paster(*args,**kwargs):
    print "Start robot for setting posters"
    robot = Robots.objects.get(name='kinopoisk_set_poster')
    print u'Checking robot %s' % robot.name
    print robot.last_start, timezone.now()

    if robot.last_start + datetime.timedelta(minutes=robot.delay) < timezone.now():
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
            poster_robot_wrapper(film_id)

    else:
        print u'Skipping robot %s' % robot.name
