from django.core.management.base import BaseCommand
from crawler.locrobots.now_or_stream_news import parse_news


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        parse_news('now_ru')