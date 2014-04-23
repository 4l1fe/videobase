# coding: utf-8

from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

from videobase import settings
from apps.films.views import test_view


urlpatterns = patterns('',
    url(r'^api/image/resize/', 'apps.films.views.resize_image'),
    url(r'^api/image/brco/', 'apps.films.views.bri_con'),
    url(r'^api/', include('apps.films.urls')),
    url(r'^api/', include('apps.users.urls')),
    url(r'^robots/', include('apps.robots.urls')),
    url(r'^api/test', test_view),
        
    # Admin
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^admin/', include(admin.site.urls)),
    # Social
    url(r'', include('social_auth.urls')),

    # Interface
    url(r'^person/', 'apps.films.views.person_view'),
    url(r'^register/', 'apps.films.views.register_view'),
    url(r'^login/', 'apps.films.views.login_view'),
    url(r'^$', 'apps.films.views.index_view'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
                            (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
