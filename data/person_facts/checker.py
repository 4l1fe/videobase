# coding: utf-8
from apps.films.models import Films
from apps.films.models import FilmExtras
from apps.films.constants import APP_FILM_TYPE_ADDITIONAL_MATERIAL_TRAILER

from apps.films.models import Countries

from data.checker import FactChecker
from data.constants import FLATLAND_NAME

person_checker = FactChecker(Films)



@film_checker.add("Person name is not in Russian")
def russian_name_check(person):
    pass

