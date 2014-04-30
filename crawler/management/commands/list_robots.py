from apps.robots.models import Robots
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        for robot in Robots.objects.all():
            print robot.name


