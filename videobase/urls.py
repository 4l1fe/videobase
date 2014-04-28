# coding: utf-8

from django.conf.urls import patterns, include, url
from django.contrib import admin
import admin_tools

from videobase import settings

from django.contrib import admin
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
    url(r'^auth/login/', 'rest_framework.authtoken.views.obtain_auth_token'),

    # Admin
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # Social
    url(r'', include('social_auth.urls')),

    # Interface
    url(r'^person/(?P<resource_id>\d+)/?$', 'apps.films.views.person_view'),
    url(r'^films?/(?P<film_id>\d+)/?$', 'apps.films.views.film_view'),
    url(r'^register/', 'apps.films.views.register_view'),
    url(r'^user/(?P<resource_id>.*)/?$', 'apps.films.views.user_view'),
    # url(r'^regi/', 'apps.films.views.login_view'),
    url(r'^$', 'apps.films.views.index_view'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
