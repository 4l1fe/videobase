# coding: utf-8
from crawler.locrobots import sites_crawler, process_film_on_site
from crawler.locrobots.amediateka_ru.loader import Amediateka_robot
from crawler.locrobots.viaplay_ru.robot import ViaplayRobot
from crawler.locrobots.playfamily_dot_ru.playfamily_xml import process
from videobase.celery import app

from crawler.tasks.utils import robot_task, robot_launch_wrapper, update_robot_state_film_id

from functools import partial

@app.task(name='amediateka_ru_robot_start')
def amediateka_robot_start(*args, **kwargs):
    '''
    Amediateka_robot
    '''
    Amediateka_robot().get_film_data()


@app.task(name='playfamily_xml')
def pltask():
    process()

@app.task(name='viaplay_ru_robot_start')
def viaplay_robot_start():
    ViaplayRobot().get_data()


@app.task(name='individual_site_film')
def launch_individual_film_site_task(site):
    robot_launch_wrapper(site, partial(process_film_on_site, site))

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


