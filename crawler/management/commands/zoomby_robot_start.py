
from crawler.utils.robot_start import process_film_on_site
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        process_film_on_site('stream_ru', 7973)

