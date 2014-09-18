from django.core.management import BaseCommand
from crawler.locrobots.itunes.itunes_robot import ItunesRobot


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        ir = ItunesRobot()
        ir.get_film_data()
