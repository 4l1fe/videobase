# coding: utf-8

from django.conf.urls import patterns, include, url

import admin_tools

from videobase import settings

from django.contrib import admin
from apps.users.views import UserAccountView, RegistrationView
from apps.users.forms import CustomRegistrationForm

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
