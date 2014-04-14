# coding: utf-8

from django.conf.urls import patterns, include, url
from django.contrib import admin
import admin_tools

from videobase import settings

from django.contrib import admin
from apps.films.views import test_view

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin_tools/', include('admin_tools.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^admin_tools/', include('admin_tools.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^api/image/resize/', 'apps.films.views.resize_image'),
                       url(r'^api/image/brco/', 'apps.films.views.bri_con'),
                       url(r'^api/', include('apps.films.urls')),
                       url(r'^api/robots/', 'apps.robots.views.schedule_api'),
                       url(r'^robots/', 'apps.robots.views.schedule_interface'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
                            (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
