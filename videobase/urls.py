# coding: utf-8

from django.conf.urls import patterns, include, url

import admin_tools
from testy_pie import v1_api
from videobase import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin/users/', include('apps.users.urls')),
                       url(r'^admin_tools/', include('admin_tools.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^admin_tools/', include('admin_tools.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       # url(r'^api/image/resize/','apps.films.views.resize_image'),
                       # url(r'^api/image/brco/','apps.films.views.bri_con'),
                       url(r'^api/', include(v1_api.urls)),
)

urlpatterns += patterns('',
                        (r'^accounts/', include('registration.urls')),
                        (r'^admin/', include(admin.site.urls)),
                    )

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
