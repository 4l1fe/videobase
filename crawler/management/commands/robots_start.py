# coding: utf-8

from django.core.management.base import BaseCommand
from optparse import make_option

from apps.films.models.films import Films
from crawler.ivi_ru.load import IVI_LoadData


class Command(BaseCommand):
    help = u'Запустить краулер'
    requires_model_validation = True
    option_list = BaseCommand.option_list + (
        make_option('--limit',
                    dest='limit',
                    help=u'How much films to process'),
    )

    def handle(self, *args, **options):
        film = Films.objects.get(pk=1)
        d = IVI_LoadData(film)
        html = d.load()