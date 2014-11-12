# coding: utf-8

from django.core.management.base import NoArgsCommand

from apps.casts.models import CastsServices

CAST_SERVICES = [

    {
        'name': 'sportbox_ru',
        'url' : 'http://news.sportbox.ru',
        'description': ''
    },
    {
        'name': 'championat_com',
        'url' : 'http://video.championat.com',
        'description': ''
    },
    {
        'name': 'liverussia_ru',
        'url' : 'http://live.russia.tv',
        'description': ''
    },
    {
        'name': 'khl_ru',
        'url' : 'http://tv.khl.ru/',
        'description': ''
    },
    {
        'name': 'ntv_plus',
        'url' : 'http://www.ntvplus.ru',
        'description': ''
    },
]


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        for cs in CAST_SERVICES:
            try:
                CastsServices.objects.get_or_create(**cs)

            except Exception,e:
                import traceback
                traceback.print_exc()

