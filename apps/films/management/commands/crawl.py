# coding: utf-8

from django.core.management.base import NoArgsCommand, CommandError
from apps.films.models import Films,PersonsFilms
from apps.users.models import Persons
from crawler.parse_page import parse_one_page
from itertools import chain 
import commands

def get_person(film,name):

    f = Persons.objects.filter(name=name)

    if f:
        print(f[0])
        return f[0]
    else:
        p = Persons(name=name)
        p.save()

        return p
    
    

    


class Command(NoArgsCommand):

    help = u'Запустить краулер'
    requires_model_validation = True

    def handle_noargs(self, **options):
        for film in Films.objects.all():
            if film.kinopoisk_id is None:
                pass
            else:
                pdata = parse_one_page(film.kinopoisk_id)

                a=[]
                for d in pdata['Films']:
                    a.extend(d.items())

                for key,value in dict(a).items():
                    setattr(film, key, value)

                film.save()

                for p in pdata['Persons']:
                    po = get_person(film,p['name'])

                    if PersonsFilms.objects.filter(film=film,person = po):
                        pass
                    else:
                        pf = PersonsFilms(person = po , film = film, p_type = p['p_type'])
                        pf.save()


                #print(pdata['Persons'])
        
