# coding: utf-8
from django.core.management.base import NoArgsCommand
from apps.films.models import Films, FilmExtras
from data.checker import FactChecker
import data.film_facts.checker


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        f = Films.objects.get(id=61)
        #Les Lapins Crétins : Retour vers le passé - Trailer HD
        #f.description = u"4 " + f.description
        #f.description = f.description + u" NOW.RU  "
        ft = FilmExtras.objects.filter(film=f)
        print f.name
        print data.film_facts.checker.film_checker.check_and_correct(f)
        print f.name