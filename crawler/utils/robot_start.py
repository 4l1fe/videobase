# coding: utf-8

"""
Module containing general functionality for crawler robots
and run function for robots written as loader parser combo
"""
from django.utils import timezone
from django.db.models import Q

from apps.films.models import Films
from apps.robots.constants import APP_ROBOTS_TRY_NO_SUCH_PAGE

from crawler.kinopoisk_ru.kinopoisk import get_id_by_film


def launch_next_robot_try_for_kinopoisk(robot):
    robot.last_start = timezone.now()
    robot.save()

    films = Films.objects.filter(~Q(robots_tries__outcome=APP_ROBOTS_TRY_NO_SUCH_PAGE),
                                 kinopoisk_id__isnull=True)[:10]
    for film in films:
        id = get_id_by_film(film)
        film.kinopoisk_id = id
        film.save()
