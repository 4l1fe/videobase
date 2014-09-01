# coding: utf-8
from django.utils import timezone

import json

from apps.robots.models import Robots
from videobase.celery import app
from apps.films.models import Films
from crawler.core.exceptions import NoSuchFilm


def get_robot_by_name(robot_name):
    try:
        return Robots.objects.get(name=robot_name)
    except Robots.DoesNotExist:
        robot = Robots(name=robot_name, last_start=timezone.now(),
                       description=' ', delay=1, state={"id": 1})
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
            pstate = json.loads(state)
        except ValueError:
            pstate = {}
    if 'id' in pstate:
        film_id = pstate['id']
        pstate['id'] += 1
        if pstate['id'] > Films.objects.count():
            pstate['id'] = 1
    else:
        pstate['id'] = 1
        film_id = 1

    robot.state = json.dumps(pstate)
    robot.last_start = timezone.now()
    robot.save()
    return film_id


def robot_launch_wrapper(robot_name, func):
        robot = get_robot_by_name(robot_name)
        item_id = update_robot_state_film_id(robot)
        print "Starting robot {} for id = {}".format(robot_name, item_id)
        try:
            return func(item_id)
        except NoSuchFilm:
            print "No Such Film"            


def robot_task(robot_name):
    def decor(func):
        @app.task(name=robot_name)
        def wrapper():
            robot_launch_wrapper(robot_name, func)
        return wrapper
    return decor