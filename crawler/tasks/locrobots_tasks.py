# coding: utf-8
from apps.films.models import Films
from apps.robots.models import Robots
from crawler.locations_saver import save_location_to_locs_dict
from crawler.locrobots import sites_crawler
from crawler.locrobots.amediateka_ru.loader import Amediateka_robot
from crawler.locrobots.process_film_from_site import process_film_on_site
from crawler.locrobots.viaplay_ru.robot import ViaplayRobot
from crawler.locrobots.playfamily_dot_ru.playfamily_xml import process
from crawler.locrobots.drugoe_kino.robot import update_drugoe_kino_listing
from crawler.locrobots.youtube_com.parser import YoutubeChannelParser
from crawler.tasks.locrobots_logging import DebugTask
from crawler.tasks.utils import robot_launch_wrapper
from crawler.utils.films_statistics import film_at_least_years_old
from crawler.utils.locations_utils import save_location, sane_dict
from videobase.celery import app
from collections import defaultdict

from django.utils import timezone

from functools import partial
import datetime


@app.task(name='amediateka_ru_robot_start', queue='amediateka_ru')
def amediateka_robot_start(*args, **kwargs):
    '''
    Amediateka_robot
    '''
    Amediateka_robot().get_film_data()


@app.task(name='playfamily_xml')
def pltask():
    process()


@app.task(name='viaplay_ru_robot_start', queue='viaplay_ru')
def viaplay_robot_start():
    ViaplayRobot().get_data()


@app.task(name='individual_site_film', base=DebugTask)
def launch_individual_film_site_task(site):
    return robot_launch_wrapper(site, partial(process_film_on_site, site))


@app.task(name='process_film_on_site')
def process_individual_film_on_site(site, film_id):
    return process_film_on_site(site, film_id)


@app.task(name='robot_launch')
def robot_launcher(*args, **kwargs):
    print 'Start'
    for robot in Robots.objects.all():
        print u'Checking robot %s' % robot.name
        if robot.last_start + datetime.timedelta(seconds=robot.delay) < timezone.now():
            if robot.name in sites_crawler:
                launch_individual_film_site_task.apply_async((robot.name,), queue=robot.name)
        else:
            print u'Skipping robot %s' % robot.name


@app.task(name='age_weighted_robot_launch')
def age_weighted_robot_launcher(years):
    print "Starting locations checks for every film at least {} days old".format(years)

    delays=defaultdict(int)

    for robot in Robots.objects.all():

        for film in Films.objects.all():
            if film_at_least_years_old(film, years):
                launch_individual_film_site_task.apply_async((robot.name,), queue=robot.name, countdown=15*delays[robot.name])
                #process_individual_film_on_site.apply_async((robot.name, film.id), countdown=15*delays[robot.name])
                delays[robot.name]+=1


@app.task(name="drugoe_kino_update")
def dg_update():
    update_drugoe_kino_listing()


@app.task(name="parse_you_tube_movies_ru", base=DebugTask, queue='you_tube_movies_ru')
def parse_you_tube_movies_ru():
    return YoutubeChannelParser.process_channels_list()

