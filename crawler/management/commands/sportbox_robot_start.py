from django.core.management import BaseCommand
from crawler.translation_robot.ntvplus_ru.parse import parse_translation


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        parse_translation()
