# coding: utf-8

from django.conf.urls import *
from apps.films.views import PersonAPIView, PersonFilmographyAPIView, PersonActionAPIView, PersonsExtrasAPIView
from rest_framework.urlpatterns import format_suffix_patterns
from apps.films.api import *


# Api patterns
v1_api_patterns = patterns('',
    url(r'^v1/films/(?P<film_id>\d+)?$', DetailFilmView.as_view(), name='film_details_view'),
    url(r'^v1/films/(?P<film_id>\d+)/locations?$', LocationsFilmView.as_view(), name='film_locations_view'),
    url(r'^v1/person/(?P<resource_id>\d+)$', PersonAPIView.as_view(), name='my_rest_view'),
    url(r'^v1/person/(?P<resource_id>\d+)/filmography$', PersonFilmographyAPIView.as_view(), name='my_rest_view'),
    url(r'^v1/person/(?P<resource_id>\d+)/action/subscribe$', PersonActionAPIView.as_view(), name='my_rest_view'),
    url(r'^v1/person/(?P<resource_id>\d+)/extras$', PersonsExtrasAPIView.as_view(), name='my_rest_view'),

)

# Format suffixes
urlpatterns = format_suffix_patterns(v1_api_patterns, suffix_required=True)
