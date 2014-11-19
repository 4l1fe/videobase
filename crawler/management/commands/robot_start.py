# coding: utf-8
from crawler.locrobots.process_film_from_site import process_film_on_site
from crawler.locrobots import sites

from django.core.management import BaseCommand

from optparse import make_option


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('-f', '--film', help=u'Id фильма'),
        make_option('-r', '--robot', help=u'Название работа',
                    choices=sites)
    )

    def handle(self, *args, **options):
        film_id = options['film']
        robot = options['robot']
        process_film_on_site('tvzavr_ru', 2)

