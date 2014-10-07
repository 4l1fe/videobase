from django.core.management.base import BaseCommand
from crawler.translation_robot.live_russia_tv.translation_live_russia_tv import parse_translation_live_russia_tv


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        parse_translation_live_russia_tv()