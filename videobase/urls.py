# coding: utf-8

from django.conf.urls import patterns, include, url

import admin_tools

from videobase import settings

from django.contrib import admin
from apps.users.views import UserAccountView, RegistrationView
from apps.users.forms import CustomRegistrationForm
from apps.films.views import PersonAPIView, PersonFilmographyAPIView
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin/users/', include('apps.users.urls')),
                       url(r'^admin_tools/', include('admin_tools.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^admin_tools/', include('admin_tools.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^api/image/resize/','apps.films.views.resize_image'),
                       url(r'^api/image/brco/','apps.films.views.bri_con'),
                       url(r'^api/', include('apps.films.urls')),
                       url(r'^api/robots/','apps.robots.views.schedule_api'),
                       url(r'^robots/','apps.robots.views.schedule_interface'),
                       url(r'^accounts/profile/', UserAccountView.as_view(), name='account_profile'),
                       url(r'^api/v1.0/person/(?P<resource_id>\d+)([/]?|[.](?P<format>\w+))$', PersonAPIView.as_view(), name='my_rest_view'),
                       url(r'^api/v1.0/resource[/]?$', PersonAPIView.as_view(), name='my_rest_view'),
                      url(r'^api/v1.0/person/(?P<resource_id>\d+)[/]filmography[.](?P<format>\w+)$', PersonFilmographyAPIView.as_view(), name='my_rest_view'),
)
urlpatterns += patterns('',

                        url(
                            r'^accounts/register/$',
                            RegistrationView.as_view(
                                form_class=CustomRegistrationForm,
                            ),
                            name='registration_register',
                        ),

                        (r'^accounts/', include('registration.urls')),
                        (r'^admin/', include(admin.site.urls)),
                    )

if settings.DEBUG:
    urlpatterns += patterns('',
                            (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
