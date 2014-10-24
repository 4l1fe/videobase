# coding: utf-8
from crawler.robots_config_generator import generate_robots_config
from django.core.management import BaseCommand
from optparse import make_option, OptionError


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option('-d', '--directory',
                    dest='directory',
                    help='Project directory'),
        make_option('-u', '--user',
                    dest='user',
                    help='Directory owner', ))

    def handle(self, *args, **kwargs):
        d, u = kwargs.get('directory'),  kwargs.get('user')
        generate_robots_config(d, u)