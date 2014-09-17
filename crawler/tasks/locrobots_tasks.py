# coding: utf-8
from apps.films.models import Films
from apps.robots.models import Robots
from crawler.locations_saver import save_location_to_locs_dict
from crawler.locrobots import sites_crawler
from crawler.locrobots.save_util import load_and_save_film_page_from_site
from crawler.locrobots.amediateka_ru.loader import Amediateka_robot
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


@app.task(name='process_film_on_site', base=DebugTask)
def process_individual_film_on_site(site, film_id):
    return process_film_on_site(site, film_id)

@app.task(name='age_weighted_robot_launch')
def age_weighted_robot_launcher(years):
    msg = "Starting locations checks for every film at least {year} days old"
    print msg.format(year=years)

    delays = defaultdict(int)
    for robot in Robots.objects.all():
        for film in Films.objects.all():
            if film_at_least_years_old(film, years):
                process_individual_film_on_site.apply_async((robot.name, film.id), countdown=15*delays[robot.name])
                delays[robot.name] += 1


@app.task(name="drugoe_kino_update")
def dg_update():
    update_drugoe_kino_listing()


@app.task(name="parse_you_tube_movies_ru", base=DebugTask, queue='you_tube_movies_ru')
def parse_you_tube_movies_ru():
    return YoutubeChannelParser.process_channels_list()


@app.task(name="load_film_from_site", queue="thor")
def load_film_page_from_site(site, film_id):
    return load_and_save_film_page_from_site(site, film_id)
