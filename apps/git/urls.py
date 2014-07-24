# coding: utf-8
from django.conf.urls import patterns, url


urlpatterns = patterns('apps.git.views',
    url(r'^info/$', 'info'),
)
