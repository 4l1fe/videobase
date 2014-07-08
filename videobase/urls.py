# coding: utf-8

from django.conf.urls import patterns, include, url
from django.contrib import admin

import admin_tools

from videobase import settings

from apps.films.views import test_view

admin.autodiscover()

urlpatterns = patterns('',
    # API
    url(r'^api/image/resize/', 'apps.films.views.resize_image'),
    url(r'^api/image/brco/', 'apps.films.views.bri_con'),
    url(r'^api/', include('apps.films.urls')),
    url(r'^api/', include('apps.users.urls')),
    url(r'^robots/', include('apps.robots.urls')),
    url(r'^api/test', test_view),

    # Interface
    url('', include('apps.films.view_url')),
    url('', include('apps.users.view_url')),

    # Auth
    url(r'', include('social_auth.urls')),

    # Admin
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^legal/$', 'apps.contents.views.legal'),
    url(r'^about/$', 'apps.contents.views.about'),

    url(r'^/rss/feed_tw/$', '')
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
