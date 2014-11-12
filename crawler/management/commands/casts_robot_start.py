from django.core.management import BaseCommand
from crawler.casts_robot import parse_sportbox_ru
from crawler.casts_robot.tasks import generic_task


class Command(BaseCommand):
    def handle(self, *args, **options):
        generic_task(parse_sportbox_ru, 'sportbox_ru')