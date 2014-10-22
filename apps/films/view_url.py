# coding: utf-8
from django.conf.urls import patterns, url

import views

urlpatterns = patterns('apps.films.views',
    # View url
    url(r'^$', views.IndexView.as_view(), name='index_view'),
    url(r'^persons/(?P<resource_id>\d+)/$', views.PersonView.as_view(), name='person_view'),
    url(r'^persons/(?P<person_id>\d+)/photo_(?P<size>\d+x\d+)/$', views.PersonsPhoto.as_view()),
    url(r'^persons/(?P<person_id>\d+)/photo/$', views.PersonsPhoto.as_view()),
    url(r'^films/(?P<film_id>\d+)/$', views.FilmView.as_view(), name='film_view'),
    url(r'^films/(?P<film_id>\d+)/action/comment$', views.CommentFilmView.as_view(), name='comment_film_view'),
    url(r'^playlist/(?P<film_id>\d+)/$', views.PlayListView.as_view(), name='playlist_film_view'),
    url(r'^playlist/$', views.PlayListView.as_view(), name='playlist_view'),
    url(r'^search/$', views.SearchView.as_view(), name='search_view'),
    url(r'^kinopoisk/(?P<film_id>\d+)/$', 'kinopoisk_view', name='kinopoisk_view'),
    url(r'^films/(?P<film_id>\d+)/poster_(?P<size>\d+x\d+)/$', views.FilmPoster.as_view()),
    url(r'^films/(?P<film_id>\d+)/poster/$', views.FilmPoster.as_view()),
)
