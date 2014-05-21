# coding: utf-8

from films_search import SearchFilmsView
from films_detail import DetailFilmView
from films_locations import LocationsFilmView
from films_persons import PersonsFilmView
from films_similar import SimilarFilmView
from films_extras import ExtrasFilmView
from films_comments import CommentsFilmView
from films_action_comment import ActCommentFilmView
from films_action_notwatch import ActNotwatchFilmView
from films_action_playlist import ActPlaylistFilmView
from films_action_rate import ActRateFilmView
from films_action_subscribe import ActSubscribeFilmView

from persons import PersonAPIView
from persons_filmography import PersonFilmographyAPIView
from persons_action import PersonActionAPIView
from persons_extras import PersonsExtrasAPIView


__all__ = [
    # Films API
    'SearchFilmsView', 'DetailFilmView', 'LocationsFilmView', 'PersonsFilmView', \
    'SimilarFilmView', 'ExtrasFilmView', 'CommentsFilmView', 'ActSubscribeFilmView', \
    'ActPlaylistFilmView', 'ActNotwatchFilmView', 'ActRateFilmView', 'ActCommentFilmView', \

    # Persons API
    'PersonAPIView', 'PersonFilmographyAPIView', 'PersonActionAPIView', 'PersonsExtrasAPIView'
]
