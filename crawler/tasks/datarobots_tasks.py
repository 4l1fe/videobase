# coding: utf-8

from __future__ import absolute_import

import datetime
from bs4 import BeautifulSoup

from django.core.files import File
from django.utils import timezone

from apps.robots.models import Robots
from apps.films.models import Persons
from apps.films.models import Films

from crawler.datarobots.kinopoisk_ru.parse_actors import PersoneParser
from crawler.datarobots.kinopoisk_ru.parse_page import get_photo
from crawler.datarobots.kinopoisk_ru.kinopoisk_poster import poster_robot_wrapper
from crawler.datarobots.imdbratings import process_all
from crawler.datarobots.kinopoisk_ru.kinopoisk_premiere import kinopoisk_news
from crawler.datarobots.youtube_com.youtube_trailers import find_youtube_trailer
from crawler.tasks.kinopoisk_one_page import kinopoisk_parse_one_film
from crawler.tor import simple_tor_get_page
from crawler.tasks.utils import update_robot_state_film_id
from videobase.celery import app

import data.film_facts.checker
from utils.common import traceback_own

KINOPOISK_LIST_FILMS_URL = "http://www.kinopoisk.ru/top/navigator/m_act%5Begenre%5D/999/m_act%5Bnum_vote%5D/10/m_act%5Brating%5D/1:/m_act%5Bis_film%5D/on/m_act%5Bis_mult%5D/on/order/year/page/{}/#results"
information_robots = ['kinopoik_robot', 'imdb_robot']


@app.task(name='persons_films_update_with_indexes')
def persons_films_update_with_indexes(kinopoisk_film_id):
    page_dump = PersoneParser.acquire_page(kinopoisk_film_id)
    PersoneParser.update_persons_films_with_indexes(page_dump, kinopoisk_film_id)


@app.task(name='kinopoisk_films')
def kinopoisk_films(pages):
    try:
        for page in range(1, pages+1):
            print u"Page number: {0} of {1}".format(page, pages)
            html = simple_tor_get_page(KINOPOISK_LIST_FILMS_URL.format(page), tor_flag=True)
            soup = BeautifulSoup(html)
            films_list = soup.findAll('div', attrs={'class': 'name'})
            for film in films_list:
                kinopoisk_id = int(film.a.get('href').split('/')[4])

                name = film.a.text
                print u"Film name: {0}".format(name)
                if u'(сериал)' in name:
                    name = name.replace(u'(сериал)', u'')

                film, flag = Films.objects.get_or_create(kinopoisk_id=kinopoisk_id,
                                                    defaults={'type': '', 'name':name})
                print u"Film: {0} {1}".format(film.name, film.kinopoisk_id)

                kinopoisk_parse_one_film.apply_async((film.kinopoisk_id, film.name))
                persons_films_update_with_indexes.apply_async((film.kinopoisk_id,))
    except Exception, e:
        traceback_own(e)


@app.task(name='kinopoisk_set_poster')
def kinopoisk_set_paster(*args, **kwargs):
    print "Start robot for setting posters"
    robot = Robots.objects.get(name='kinopoisk_set_poster')

    if robot.last_start + datetime.timedelta(seconds=robot.delay) < timezone.now():
        film_id = update_robot_state_film_id(robot)
        poster_robot_wrapper(film_id)

    else:
        print u'Skipping robot {name}'.format(name=robot.name)


@app.task(name='imdb_rating_update')
def imdb_robot_start(*args, **kwargs):
    process_all()


def film_at_least_years_old(film, years):
    '''
    Returns true if @film less than @years old
    '''
    return timezone.now().date() - film.release_date < timezone.timedelta(days=365 * years)


def film_checked_on_kp_at_least_days_ago(film, days):
    '''
    Returns true if @film last checked on kinopoisk more than  @days ago
    '''
    if film.kinopoisk_lastupdate:
        return timezone.now() - film.kinopoisk_lastupdate > timezone.timedelta(days=days)
    else:
        return True


@app.task(name='kinopoisk_refresher')
def create_due_refresh_tasks():
    for film in Films.objects.all():
        if film_at_least_years_old(film, years=2):
            if film_checked_on_kp_at_least_days_ago(film, days=3):
                kinopoisk_parse_one_film.apply_async((film.kinopoisk_id, film.name))

        elif film_at_least_years_old(film, years=4):
            if film_checked_on_kp_at_least_days_ago(film, days=7):
                kinopoisk_parse_one_film.apply_async((film.kinopoisk_id, film.name))

        else:
            if film_checked_on_kp_at_least_days_ago(film, days=14):
                kinopoisk_parse_one_film.apply_async((film.kinopoisk_id, film.name))


@app.task(name='kinopoisk_news')
def parse_kinopoisk_news():
    '''
    Periodic task for parsing new films from kinopoisk
    For each film found on premiere page, parser called asynchronously
    '''
    for name, kinopoisk_id in kinopoisk_news():
        kinopoisk_parse_one_film.apply_async((kinopoisk_id, name))


@app.task(name="find_trailer_for_film")
def find_trailer(film_id):
    film = Films.objects.get(id=film_id)
    find_youtube_trailer(film)

@app.task(name='youtube_trailers_all')
def trailer_commands():
    for film in Films.objects.all():
        find_trailer.apply_async((film.id,))

@app.task(name='check_one_film_by_id')
def check_and_correct_one_film(film_id):
    film = Films.objects.get(id=film_id)
    data.film_facts.checker.film_checker.check_and_correct(film)

@app.task(name='check_one_person_by_id')
def check_and_correct_one_person(person_id):
    person = Persons.objects.get(id=person_id)
    data.person_facts.checker.person_checker.check_and_correct(person)

@app.task(name='film_info_check_and_correct')
def check_and_correct_tasks():
    for film in Films.objects.all():
        check_and_correct_one_film.apply_async(film.id)

@app.task(name='persons_check_and_correct')
def person_check_and_correct_tasks():
    for person in Persons.objects.all():
        check_and_correct_one_person.apply_async(person.id)

