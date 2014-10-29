# coding: utf-8

from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns

from apps.films.api import *

v1_api_patterns = patterns('',
    # Films API
    url(r'^v1/films/search$', SearchFilmsView.as_view(), name='film_search_view'),
    url(r'^v1/films/(?P<film_id>\d+)$', DetailFilmView.as_view(), name='film_details_view'),
    url(r'^v1/films/(?P<film_id>\d+)/persons', PersonsFilmView.as_view(), name='film_persons_view'),
    url(r'^v1/films/(?P<film_id>\d+)/locations$', LocationsFilmView.as_view(), name='film_locations_view'),
    url(r'^v1/films/(?P<film_id>\d+)/similar$', SimilarFilmView.as_view(), name='film_similar_view'),
    url(r'^v1/films/(?P<film_id>\d+)/extras$', ExtrasFilmView.as_view(), name='film_extras_view'),
    url(r'^v1/films/(?P<film_id>\d+)/comments$', CommentsFilmView.as_view(), name='film_comments_view'),
    url(r'^v1/films/(?P<film_id>\d+)/action/subscribe$', ActSubscribeFilmView.as_view(), name='act_film_subscribe_view'),
    url(r'^v1/films/(?P<film_id>\d+)/action/playlist$', ActPlaylistFilmView.as_view(), name='act_film_playlist_view'),
    url(r'^v1/films/(?P<film_id>\d+)/action/notwatch$', ActNotwatchFilmView.as_view(), name='act_film_notwatch_view'),
    url(r'^v1/films/(?P<film_id>\d+)/action/rate$', ActRateFilmView.as_view(), name='act_film_rate_view'),
    url(r'^v1/films/(?P<film_id>\d+)/action/comment$', ActCommentFilmView.as_view(), name='act_film_comment_view'),

    # Person API
    url(r'^v1/persons/(?P<resource_id>\d+)$', PersonAPIView.as_view(), name='person_api_view'),
    url(r'^v1/persons/(?P<resource_id>\d+)/filmography$', PersonFilmographyAPIView.as_view(), name='person_filmography_view'),
    url(r'^v1/persons/(?P<resource_id>\d+)/action/subscribe$', PersonActionAPIView.as_view(), name='person_action_view'),
    url(r'^v1/persons/(?P<resource_id>\d+)/extras$', PersonsExtrasAPIView.as_view(), name='person_extras_view'),
)

# Format suffixes
urlpatterns = format_suffix_patterns(v1_api_patterns, suffix_required=True)
