# coding: utf-8

from django.conf.urls import patterns, url


urlpatterns = patterns('apps.rss.views',
    url(r'^feed_tw/$', 'get_feed_tw'),
    url(r'^feed_vk/$', 'get_feed_vk'),
    url(r'^feed/$', 'get_feed'),
    url(r'^feed_fb/$', 'get_feed_fb'),
    url(r'^feed_comment/$', 'get_feed_comment')
)
