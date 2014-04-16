# coding: utf-8

from django.conf.urls import patterns, url

from apps.users.views import ObtainSessionToken, RevokeSessionToken, ObtainAuthToken
from apps.users.api import *

from rest_framework.urlpatterns import format_suffix_patterns

v1_api_patterns = patterns('',
    # Auth API
    url(r'^v1/auth/session?$', ObtainSessionToken.as_view()),
    url(r'^v1/auth/login?$', ObtainAuthToken.as_view()),
    url(r'^v1/auth/revoke?$', RevokeSessionToken.as_view(), name='revoke'),
    # User API
    url(r'^v1/user/info?$', UserInfoView.as_view(), name='user_info'),
    url(r'^v1/user/password?$', UserChangePasswordView.as_view(), name='user_change_password'),
    # Users API
    url(r'^v1/users/(?P<user_id>\d+)/friendship?$', UsersFriendshipView.as_view(), name='user_friendship_action'),
    url(r'^v1/users/(?P<user_id>\d+)/films?$', UsersFilmsView.as_view(), name='user_films'),
)

urlpatterns = format_suffix_patterns(v1_api_patterns, suffix_required=True)