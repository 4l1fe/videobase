# coding: utf-8

from django.conf.urls import patterns, url

from apps.users.api import *
from apps.users.views import tokenize_view
from rest_framework.urlpatterns import format_suffix_patterns

v1_api_patterns = patterns('',
    # Auth API
    url(r'^v1/auth/session$', ObtainSessionToken.as_view(), name='session'),
    url(r'^v1/auth/login$', ObtainAuthToken.as_view(), name='login'),
    url(r'^v1/auth/revoke$', RevokeSessionToken.as_view(), name='revoke'),
    # User API
    url(r'^v1/user/info?$', UserInfoView.as_view(), name='user_info'),
    url(r'^v1/user/password?$', UserChangePasswordView.as_view(), name='user_change_password'),
    # Users API
    url(r'^v1/users/(?P<user_id>\d+)$', UsersView.as_view(), name='users'),
    url(r'^v1/users/(?P<user_id>\d+)/friendship$', UsersFriendshipView.as_view(), name='users_friendship_action'),
    url(r'^v1/users/(?P<user_id>\d+)/friends$', UsersFriendsView.as_view(), name='users_friends'),
    url(r'^v1/users/(?P<user_id>\d+)/films$', UsersFilmsView.as_view(), name='users_films'),
    url(r'^v1/users/(?P<user_id>\d+)/persons$', UsersPersonsView.as_view(), name='users_persons'),
    url(r'^v1/users/(?P<user_id>\d+)/genres$', UsersGenresView.as_view(), name='users_genres'),
)

urlpatterns = format_suffix_patterns(v1_api_patterns, suffix_required=True)