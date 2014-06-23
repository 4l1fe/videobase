# coding: utf-8

from django.conf.urls import patterns, include, url
from django.contrib import admin
import admin_tools

from django.contrib import admin

from videobase import settings
from apps.users import views
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
    url(r'^$', 'apps.films.views.index_view', name='index_view'),
    url(r'^register/$', views.RegisterUserView.as_view()),
    url(r'^restore-password/$', views.RestorePasswordView.as_view()),
    url(r'^login/$', views.LoginUserView.as_view(), name='login_view'),
    url(r'^user/profile/$', views.UserProfileView.as_view(), name='profile_view'),
    url(r'^user/(?P<user_id>\d+)/$', views.UserView.as_view()),
    url(r'^feed/$', 'apps.users.views.feed_view', name='user_feed_view'),
    url(r'^persons/(?P<resource_id>\d+)/$', 'apps.films.views.person_view', name='person_view'),
    url(r'^films/(?P<film_id>\d+)/$', 'apps.films.views.film_view', name='film_view'),
    url(r'^playlist/(?P<film_id>\d+)/$', 'apps.films.views.playlist_view', name='playlist_film_view'),
    url(r'^playlist/$', 'apps.films.views.playlist_view', name='playlist_view'),
    url(r'^kinopoisk/(?P<film_id>\d+)/$', 'apps.films.views.kinopoisk_view', name='kinopoisk_view'),

    # Auth
    url(r'', include('social_auth.urls')),
    url('^tokenize/?$', views.TokenizeView.as_view(), name="tokenize"),

    # Admin
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
