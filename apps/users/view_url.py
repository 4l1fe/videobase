# coding: utf-8

from django.conf.urls import patterns, url
from apps.users import views


urlpatterns = patterns('',
    url(r'^restore-password/$', views.RestorePasswordView.as_view()),
    url(r'^profile/$', views.UserProfileView.as_view(), name='profile_view'),
    url(r'^users/(?P<user_id>\d+)/$', views.UserView.as_view()),
    url(r'^stream/$', views.FeedView.as_view(), name='user_feed_view'),
    url(r'^register/$', views.RegisterUserView.as_view()),
    url(r'^logout/(?P<provider>[a-zA-Z0-9-]+)/$', views.delete_social_provider),

    # Auth
    url(r'^login/$', views.LoginUserView.as_view(), name='login_view'),
    url(r'^logout/$', views.UserLogoutView.as_view(), name='logout_view'),
    url(r'^tokenize/?$', views.TokenizeView.as_view(), name="tokenize"),
)

