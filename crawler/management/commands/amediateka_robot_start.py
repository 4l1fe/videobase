from django.core.management.base import NoArgsCommand
from apps.films.models import Films
from crawler.locrobots.tvigle_ru.loader import  TVIGLE_Loader
from crawler.tor import simple_tor_get_page
from crawler.locrobots.individual_tasks import process_individual_film_on_site


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        film = Films.objects.get(id=59124)
        process_individual_film_on_site.run('tvigle_ru', 6350)
        am_load = TVIGLE_Loader(film)
        am_load.get_url(simple_tor_get_page)


