# coding: utf-8

from django.conf.urls import patterns, url

urlpatterns = patterns('apps.robots.views',
    url(r'^$', 'schedule_interface', name='robots_interface'),
)
