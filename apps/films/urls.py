# coding: utf-8

from django.conf.urls import *

from rest_framework.urlpatterns import format_suffix_patterns

from apps.films.api import DetailFilmView


# Api patterns
api_patterns = patterns('',
    url(r'^v1/film/(?P<film_id>\d+)?$', DetailFilmView.as_view(), name='film_detail_view')
)

# Format suffixes
urlpatterns = format_suffix_patterns(api_patterns, suffix_required=True)
