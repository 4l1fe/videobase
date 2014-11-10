# coding: utf-8

from django.apps import AppConfig


class UserConfig(AppConfig):
    name = 'apps.users'

    def ready(self):

        # import signal
        import apps.users.signals
