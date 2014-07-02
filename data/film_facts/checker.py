# coding: utf-8
from apps.films.models import Films

from apps.films.models import Countries

from data.checker import FactChecker
from data.constants import FLATLAND_NAME

film_checker = FactChecker(Films)


@film_checker.add('Flatland in countries')
def flatland_check(film):
    flatland = Countries.objects.get(name = FLATLAND_NAME)
    return not ( flatland in film.countries.all() )







