# coding: utf-8

from django.apps import AppConfig


class MyAppConfig(AppConfig):
    name = 'apps.users'

    def ready(self):

        # import signal
        import apps.users.signals
