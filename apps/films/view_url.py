# coding: utf-8

from django.conf.urls import patterns, url

urlpatterns = patterns('apps.films.views',
    # View url
    url(r'^$', 'index_view', name='index_view'),
    url(r'^persons/(?P<resource_id>\d+)/$', 'person_view', name='person_view'),
    url(r'^films?/(?P<film_id>\d+)/$', 'film_view', name='film_view'),
    url(r'^playlist/(?P<film_id>\d+)/$', 'playlist_view', name='playlist_film_view'),
    url(r'^playlist/$', 'playlist_view', name='playlist_view'),
    url(r'^kinopoisk/(?P<film_id>\d+)/$', 'kinopoisk_view', name='kinopoisk_view'),
    url(r'^search/$', 'search_view', name='search_view'),
)
