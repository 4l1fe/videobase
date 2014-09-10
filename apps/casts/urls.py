# coding: utf-8

from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns

from apps.casts.api import CastsListView, CastsInfoView, CastsExtraView, CastsSubscribeView, \
    CastsChatSendView, CastsRatingView, CastsChatsMsgsView, CastsChatsUsersView


v1_api_patterns = patterns('',
    url(r'^v1/casts/list', CastsListView.as_view(), name='cast_list_view'),
    url(r'^v1/casts/(?P<cast_id>\d+)/info', CastsInfoView.as_view(), name='cast_info_view'),
    url(r'^v1/casts/(?P<cast_id>\d+)/extras', CastsExtraView.as_view(), name='cast_extras_view'),
    url(r'^v1/casts/(?P<cast_id>\d+)/rating$', CastsRatingView.as_view(), name='cast_rating_view'),
    url(r'^v1/casts/(?P<cast_id>\d+)/subscribe$', CastsSubscribeView.as_view(), name='cast_subscribe_view'),
    url(r'^v1/castchats/(?P<castchat_id>\d+)/msgs$', CastsChatsMsgsView.as_view(), name='castchat_msgs'),
    url(r'^v1/castchats/(?P<cast_id>\d+)/send$', CastsChatSendView.as_view(), name='castchat_send_view'),
    url(r'^v1/castchats/(?P<castchat_id>\d+)/users$', CastsChatsUsersView.as_view(), name='castchat_users'),
)

urlpatterns = format_suffix_patterns(v1_api_patterns, suffix_required=True)
