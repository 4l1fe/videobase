from django.core.management.base import BaseCommand
from crawler.locrobots.news import parse_news


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        parse_news('now_ru')