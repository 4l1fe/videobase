# coding: utf-8

from films_search import FilmsSearchResource
from films_detail import DetailFilmView
from films_locations import LocationsFilmView
from films_persons import PersonsFilmView
from films_semilar import SimilarFilmView
from films_extras import ExtrasFilmView
from films_comments import CommentsFilmView


__all__ = [
    'FilmsSearchResource', 'DetailFilmView', 'LocationsFilmView', 'PersonsFilmView', \
    'SimilarFilmView', 'ExtrasFilmView', 'CommentsFilmView', \
]
