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
                    help='Directory owner'),
        make_option('-f', '--filename',
                    dest='filename',
                    help='Absolute or relative config file name')
    )

    def handle(self, *args, **kwargs):
        gen_kwargs = {}
        d = kwargs.get('directory'); if d:
            gen_kwargs.update(dict(directory=d))
        u = kwargs.get('user'); if u:
            gen_kwargs.update(dict(user=u))
        fn = kwargs.get('filename'); if fn:
            gen_kwargs.update(dict(filename=fn))

        generate_robots_config(**gen_kwargs)