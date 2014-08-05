# coding: utf-8
from django.core.management.base import NoArgsCommand
from apps.films.models import Films, FilmExtras
from apps.films.models import Persons
# import data.film_facts.checker
import data.person_facts.checker


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        f = Films.objects.get(id=33665)
        #person = Persons.objects.get(kinopoisk_id=23344 ) #1735
        #Les Lapins Crétins : Retour vers le passé - Trailer HD
        #f.description = u"4 " + f.description
        #f.description = f.description + u" NOW.RU  "
        #ft = FilmExtras.objects.filter(film=f)
        #print f.name
        #print data.film_facts.checker.film_checker.check_and_correct(f)
        #print f.name
        #person.kinopoisk_id = 1554040
        #person.save()
        print(data.film_facts.checker.film_checker.check_and_correct(f))
        #print(data.person_facts.checker.person_checker.check_and_correct(person))
        #print(person.name, person.photo.size, person.bio, person.kinopoisk_id)