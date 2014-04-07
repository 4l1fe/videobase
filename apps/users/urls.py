# coding: utf-8

from django.conf.urls import patterns, url

from .views import RegisterUserView

urlpatterns = patterns('apps.users.views',
    # Регистрация
    (r'^register/$', RegisterUserView.as_view()),

    # Востановление пароля
    (r'^restore_password/$', 'restore_password')
)
