# coding: utf-8
from apps.robots.models import Robots

__author__ = 'vladimir'


def create_queue_str(robot_name):
    return "python manage.py celery worker -Q {} \n".format(robot_name)


def generate_config_file():
    result_file_name = ''
    f = open('robots_config', 'w')
    for robot in Robots.objects.all():
        f.write(create_queue_str(robot.name))
    result_file_name = 'robots_config'
    return result_file_name