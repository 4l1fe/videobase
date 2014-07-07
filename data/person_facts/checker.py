# coding: utf-8
from apps.films.models import Films
from apps.films.models import FilmExtras
from apps.films.constants import APP_FILM_TYPE_ADDITIONAL_MATERIAL_TRAILER

from apps.films.models import Countries

from data.checker import FactChecker
from data.constants import FLATLAND_NAME

import gdata.youtube
import gdata.youtube.service

film_checker = FactChecker(Films)



@film_checker.add('Flatland in countries')
def flatland_check(film):
    flatland = Countries.objects.get(name = FLATLAND_NAME)
    return not ( flatland in film.countries.all() )

@film_checker.add('First trailer name doesnt contain name of films')
def trailer_name_check(film):

    film_trailers = FilmsExtras.objects.filter(type = APP_FILM_TYPE_ADDITIONAL_MATERIAL_TRAILER)

    ft = film_trailers[0]

    yid = re.match('.+watch[?]v[=](?P<id>.+)(([&].+)?)', ft.url)
    #return film.name in






