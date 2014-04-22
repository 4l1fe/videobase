# coding: utf-8
from __future__ import absolute_import
from apps.robots.models import Robots
from celery import shared_task
from django.utils import timezone
from crawler.robot_start import launch_next_robot_try, sites_crawler

import datetime
import logging
from videobase.celery import app
from celery.utils.log import get_task_logger


information_robots = ['kinopoik_robot','imdb_robot']


logger = get_task_logger(__name__)


@app.task(name='robot_launch')
def robot_launcher(*args,**kwargs):

    print 'Start'

    for robot in Robots.objects.all():
        print u'Checking robot %s' % robot.name
        print robot.last_start, timezone.now()
        if robot.last_start + datetime.timedelta(minutes=5) < timezone.now():

            if robot.name in sites_crawler:
                launch_next_robot_try(site=robot.name)
        else:
            print u'Skipping robot %s' % robot.name






