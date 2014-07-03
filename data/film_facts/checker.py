# coding: utf-8
from datetime import datetime
from apps.films.models import Films, FilmExtras

from apps.films.models import Countries

from data.checker import FactChecker
from data.constants import FLATLAND_NAME
import gdata.youtube
import gdata.youtube.service
import re


film_checker = FactChecker(Films)


@film_checker.add(u"Release date differs from omdb one by more than a year")
def omdb_year_check(film):
    pass


@film_checker.add("There is no such trailer")
def trailer_check(film):
    pass

@film_checker.add("Youtube trailer duration not within limits")
def trailer_duration_check(film):
    pass


@film_checker.add("Film release year is not 2014")
def film_release_date_check(film):
    date_string = '2014'
    date = datetime.strptime(date_string, '%Y')
    return film.release_date.year == date.year

    
    





