# coding: utf-8

from django.conf.urls import patterns, url

from apps.users.views import LogentrySummaryView


urlpatterns = patterns('',
                       url(r'^logentry_summary/$', LogentrySummaryView.as_view(), name='logentry_summary'),
)
