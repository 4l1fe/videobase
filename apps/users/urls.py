# coding: utf-8

from django.conf.urls import patterns, url

from apps.users.views import ObtainSessionToken

from rest_framework.urlpatterns import format_suffix_patterns

v1_api_patterns = patterns('',
    url(r'^v1/auth/session$', ObtainSessionToken.as_view()),
    url(r'^v1/auth/login/', 'rest_framework.authtoken.views.obtain_auth_token'),
)

urlpatterns = format_suffix_patterns(v1_api_patterns, suffix_required=True)