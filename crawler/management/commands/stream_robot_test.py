from django.core.management.base import BaseCommand
from crawler.locrobots.tvzor_news import parse_tvzor_news


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        parse_tvzor_news()