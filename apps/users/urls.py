# coding: utf-8

from django.conf.urls import patterns, url

from apps.users.views import ObtainSessionToken
from apps.users.api import *

from rest_framework.urlpatterns import format_suffix_patterns

v1_api_patterns = patterns('',
    url(r'^v1/auth/session$', ObtainSessionToken.as_view()),
    url(r'^v1/auth/login/', 'rest_framework.authtoken.views.obtain_auth_token'),

    # Users API
    url(r'^v1/users/(?P<user_id>\d+)/friendship?$', UsersFriendshipView.as_view(), name='user_friendship_action')
)

urlpatterns = format_suffix_patterns(v1_api_patterns, suffix_required=True)