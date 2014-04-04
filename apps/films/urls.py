# coding: utf-8

from django.conf.urls import *
from rest_framework.urlpatterns import format_suffix_patterns

from apps.films.api import *


# Api patterns
v1_api_patterns = patterns('',
    url(r'^v1/films/(?P<film_id>\d+)?$', DetailFilmView.as_view(), name='film_details_view'),
    url(r'^v1/films/(?P<film_id>\d+)/persons?$', PersonsFilmView.as_view(), name='film_persons_view'),
    url(r'^v1/films/(?P<film_id>\d+)/locations?$', LocationsFilmView.as_view(), name='film_locations_view'),
    url(r'^v1/films/(?P<film_id>\d+)/semilar?$', SimilarFilmView.as_view(), name='film_semilar_view'),
    url(r'^v1/films/(?P<film_id>\d+)/extras?$', ExtrasFilmView.as_view(), name='film_extras_view'),
)

# Format suffixes
urlpatterns = format_suffix_patterns(v1_api_patterns, suffix_required=True)
