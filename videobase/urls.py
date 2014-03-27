# coding: utf-8

from django.conf.urls import patterns, include, url

from videobase import settings

import admin_tools

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin/users/', include('apps.users.urls')),
                       url(r'^admin_tools/', include('admin_tools.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^admin_tools/', include('admin_tools.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^api/image/resize/','apps.films.views.resize_image'),
                       url(r'^api/image/brco/','apps.films.views.bri_con'),
)

urlpatterns += patterns('',
                        (r'^accounts/', include('registration.urls')),
                        (r'^admin/', include(admin.site.urls)),
                    )

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
