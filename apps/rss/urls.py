# coding: utf-8

from django.conf.urls import patterns, url


urlpatterns = patterns('apps.rss.views',
    url(r'^feed(?P<social>_tw|_vk|_fb|_ok|_comment)?/$', 'feed_view'),
)
