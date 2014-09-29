# coding: utf-8

from django.conf.urls import patterns, include, url
from django.contrib import admin

from videobase import settings

from apps.films.views import test_view
from apps.users.views import feed_view

admin.autodiscover()

urlpatterns = patterns('',
    # API
    url(r'^api/image/resize/', 'apps.films.views.resize_image'),
    url(r'^api/image/brco/', 'apps.films.views.bri_con'),
    url(r'^api/', include('apps.films.urls', namespace='films_api')),
    url(r'^api/', include('apps.users.urls', namespace='users_api')),
    url(r'^api/', include('apps.casts.urls', namespace='casts_api')),
    url(r'^robots/', include('apps.robots.urls')),
    url(r'^api/test', test_view),

    # Interface
    url('', include('apps.films.view_url')),
    url('', include('apps.users.view_url')),

    # OAuth
    url(r'', include('social.apps.django_app.urls', namespace='social')),

    # Admin
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^legal/$', 'apps.contents.views.legal'),
    url(r'^about/$', 'apps.contents.views.about'),

    # RSS
    url(r'^rss/', include('apps.rss.urls')),

    # GIT
    url(r'^git/', include('apps.git.urls')),

    # notice_feed_letter
    url(r'^mail/notice_feed_letter/', feed_view),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
