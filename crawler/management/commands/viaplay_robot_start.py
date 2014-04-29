from django.core.management.base import BaseCommand, NoArgsCommand
from crawler.viaplay_ru.robot import ViaplayRobot
from crawler.robot_start import launch_next_robot_try


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        viaplay_robot = ViaplayRobot()
        viaplay_robot.get_data()
