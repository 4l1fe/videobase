# coding: utf-8
from apps.films.models import Films
from apps.robots.models import Robots
from crawler.locrobots import sites_crawler
from crawler.locrobots.itunes.itunes_robot import ItunesRobot
from crawler.locrobots.amediateka_ru.loader import Amediateka_robot
from crawler.locrobots.mail_ru.mail_robot import MailRobot
from crawler.locrobots.viaplay_ru.robot import ViaplayRobot
from crawler.locrobots.playfamily_dot_ru.playfamily_xml import process
from crawler.locrobots.drugoe_kino.robot import update_drugoe_kino_listing
from crawler.locrobots.youtube_com.parser import YoutubeChannelParser
from crawler.tasks.locrobots_logging import DebugTask
from crawler.utils.films_statistics import film_at_least_years_old
from videobase.celery import app
from collections import defaultdict
from crawler.locrobots.individual_tasks import process_individual_film_on_site
from crawler.locrobots.now_or_stream_news import parse_news
from crawler.locrobots.tvzor_news import parse_tvzor_news


@app.task(name='amediateka_robot_start')
def amediateka_robot_start(*args, **kwargs):
    '''
    Amediateka_robot
    '''
    Amediateka_robot().get_film_data()


@app.task(name='itunes_robot_start')
def itunes_robot_start():
    ItunesRobot().get_film_data()


@app.task(name='mail_robot_start')
def mail_robot_start():
    MailRobot.get_film_data()


@app.task(name='pltask')
def pltask():
    process()


@app.task(name='viaplay_robot_start')
def viaplay_robot_start():
    ViaplayRobot().get_data()


@app.task(name='age_weighted_robot_launcher')
def age_weighted_robot_launcher(years):
    msg = "Starting locations checks for every film at least {year} days old"
    print msg.format(year=years)
    delays = defaultdict(int)
    for film in Films.objects.all():
        #ПОМЕНЯТЬ МЕСТАМИ ЦИКЛЫ
        for robot in Robots.objects.all():
            if film_at_least_years_old(film, years):
                if robot.name in sites_crawler:
                    process_individual_film_on_site.apply_async((robot.name, film.id), countdown=15*delays[robot.name], queue=robot.name)
                    delays[robot.name] += 1


@app.task(name="dg_update")
def dg_update():
    update_drugoe_kino_listing()


@app.task(name="parse_you_tube_movies_ru", base=DebugTask)
def parse_you_tube_movies_ru():
    return YoutubeChannelParser.process_channels_list()


@app.task(name="parse_news_from_now_ru")
def parse_news_from_now_ru():
    robot = 'now_ru'
    now_news = parse_news('robot')
    for film in now_news:
        process_individual_film_on_site.apply_async(args=(robot, film['film_id'], film['url']))


@app.task(name="parse_news_from_stream_ru")
def parse_news_from_stream_ru():
    robot = 'stream_ru'
    stream_news = parse_news('robot')
    for film in stream_news:
        process_individual_film_on_site.apply_async(args=(robot, film['film_id'], film['url']))


@app.task(name="parse_news_from_tvzor_ru")
def parse_news_from_tvzor_ru():
    robot = 'tvzor_ru'
    tvzor_news = parse_tvzor_news()
    for film in tvzor_news:
        process_individual_film_on_site.apply_async(args=(robot, film['film_id'], film['url']))
