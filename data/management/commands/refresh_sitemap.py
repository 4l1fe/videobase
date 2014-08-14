# coding: utf-8
from django.core.management.base import NoArgsCommand
from data.sitemap import refresh


class Command(NoArgsCommand):
    def handle_noargs(self, **options):

        refresh()
        