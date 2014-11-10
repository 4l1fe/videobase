from django.core.management.base import NoArgsCommand
from crawler.locrobots.individual_tasks import process_individual_film_on_site


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
         process_individual_film_on_site.run('tvigle_ru', 59124)



