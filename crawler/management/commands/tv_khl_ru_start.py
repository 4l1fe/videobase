# coding: utf-8
from crawler.casts_robot.tv_khl_ru.parse import TvKHLRuParser

__author__ = 'vladimir'

from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        TvKHLRuParser.get_translations()
