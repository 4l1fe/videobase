from django.contrib import admin
from django.conf.urls import patterns, include, url

# import admin_tools

from videobase import settings



admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'videobase.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    # url(r'^admin_tools/', include('admin_tools.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )