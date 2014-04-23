__author__ = 'denis'
from django.core.management.base import NoArgsCommand
from django.template import Template, Context
from django.conf import settings
from apps.robots.models import  RobotsTries

from crawler.robot_start import launch_next_robot_try as handle, sites_crawler
class Command(NoArgsCommand):
    def handle_noargs(self, **options):

        [robot_try.delete() for robot_try in RobotsTries.objects.all()]
        for site in ['ivi_ru',]:# sites_crawler: #['now_ru']:

            handle( site, film_id = 65)