# coding: utf-8

from films_search import FilmsSearchResource
from films_detail import DetailFilmView
from films_locations import LocationsFilmView
from films_persons import PersonsFilmView
from films_semilar import SimilarFilmView
from films_extras import ExtrasFilmView
from films_comments import CommentsFilmView
from films_action_comment import ActCommentFilmView
from films_action_notwatch import ActNotwatchFilmView
from films_action_playlist import ActPlaylistFilmView
from films_action_rate import ActRateFilmView
from films_action_subscribe import ActSubscribeFilmView


__all__ = [
    'FilmsSearchResource', 'DetailFilmView', 'LocationsFilmView', 'PersonsFilmView', \
    'SimilarFilmView', 'ExtrasFilmView', 'CommentsFilmView', 'ActSubscribeFilmView', \
    'ActPlaylistFilmView', 'ActNotwatchFilmView', 'ActRateFilmView', 'ActCommentFilmView', \
]
