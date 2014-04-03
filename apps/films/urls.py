# coding: utf-8

from rest_framework.urlpatterns import format_suffix_patterns
from apps.films.api import DetailFilmView
from django.conf.urls import *

urlpatterns = patterns('',
    url(r'^v1/film/(?P<film_id>\d+)?$', DetailFilmView.as_view(), name='film_detail_view')
)

urlpatterns = format_suffix_patterns(urlpatterns, suffix_required=True)
