from django.core.management import BaseCommand
from crawler.casts_robot import parse_sportbox_ru, parse_khl
from crawler.casts_robot.tasks import generic_task


class Command(BaseCommand):
    def handle(self, *args, **options):
        generic_task(parse_khl, 'khl_ru')