
from bs4 import BeautifulSoup

from django.core.files import File

from apps.films.models import Persons

from crawler.datarobots.kinopoisk_ru.parse_page import get_photo, traceback_own
from crawler.tasks.utils import robot_task
from crawler.tor import simple_tor_get_page
from crawler.datarobots.kinopoisk_ru.parse_actors import update_kinopoisk_persone

@robot_task('parse_kinopoisk_persons')
def parse_kinopoisk_persons(pid):
    update_kinopoisk_persone(pid)


