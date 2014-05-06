from django.core.management.base import BaseCommand, NoArgsCommand
from crawler.ayyo_ru.robot import AyyoRobot


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        viaplay_robot = AyyoRobot(63)
        viaplay_robot.get_data()