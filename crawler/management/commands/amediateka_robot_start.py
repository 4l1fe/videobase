from crawler.amediateka_ru.loader import Amediateka_robot
from crawler.mosfilm_ru.loader import MosfilmRobot
from django.core.management.base import NoArgsCommand
from apps.robots.models import  RobotsTries, Robots
from crawler.robot_start import launch_next_robot_try as handle, sites_crawler
from crawler.amediateka_ru.loader import  *

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        mosfilm_load = MosfilmRobot(3777)
        mosfilm_load.get_data()

