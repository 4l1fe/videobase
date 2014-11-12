# coding: utf-8
from django.core.management.base import BaseCommand
from crawler.robot_start import launch_next_robot_try


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        launch_next_robot_try('ivi_ru', 2367)