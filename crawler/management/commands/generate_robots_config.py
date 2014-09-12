# coding: utf-8
from crawler.robots_config_generator import generate_config_file

__author__ = 'vladimir'

from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        generate_config_file()