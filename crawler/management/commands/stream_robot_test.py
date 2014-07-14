from django.core.management.base import BaseCommand
from crawler.locrobots.ayyo_ru.robot import AyyoRobot
from apps.films.models.persons import Persons


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        robot = AyyoRobot(28)
        robot.get_data()