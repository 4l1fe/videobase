# coding: utf-8
from django.core.management.base import NoArgsCommand
from apps.films.models import Films, FilmExtras
from data.checker import FactChecker
import data.film_facts.checker


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        f = Films.objects.get(pk=91)
        f.description = u"4 " + f.description
        #f.description = f.description + u" NOW.RU  "
        ft = FilmExtras.objects.filter(film=f)
        print f.description
        print data.film_facts.checker.film_checker.check_and_correct(f)
        print f.description