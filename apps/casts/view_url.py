# coding: utf-8

from django.conf.urls import patterns, url
from apps.casts import views


urlpatterns = patterns('',
    url(r'^casts/$', views.CastsView.as_view(), name='casts_view'),
    url(r'^casts/(?P<cast_id>\d+)/$', views.CastInfoView.as_view(), name='cast_info'),
)
