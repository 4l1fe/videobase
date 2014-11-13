# coding: utf-8
from apps.robots.models import Robots
from django.core.management.base import NoArgsCommand


class Command(NoArgsCommand):

    def handle(self, *args, **kwargs):

        for robot in Robots.objects.all():
            print robot.name


