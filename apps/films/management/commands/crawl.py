# coding: utf-8

from django.core.management.base import BaseCommand, CommandError
from apps.films.models import Films,PersonsFilms,Persons
from apps.films.constants import APP_PERSON_PHOTO_DIR,APP_FILM_CRAWLER_LIMIT,APP_FILM_CRAWLER_DELAY
from apps.robots.models import KinopoiskTries
from apps.robots.constants import APP_ROBOT_FAIL, APP_ROBOT_SUCCESS
from crawler.parse_page import parse_one_page
from django.core.files import File
from itertools import chain
from optparse import make_option
import datetime
import os
from time import sleep


LIMIT = 10
def get_person(film,name):

    f = Persons.objects.filter(name=name)

    if f:
        return f[0]
    else:
        p = Persons(name=name,photo='')
        print p.id
        p.save()

        return p

class Command(BaseCommand):

    help = u'Запустить краулер'
    requires_model_validation = True
    option_list = BaseCommand.option_list + (
        make_option('--limit',
            dest = 'limit',
            default = APP_FILM_CRAWLER_LIMIT,
            help = u'How much films to process'),
        )

    def handle(self,*args, **options):
        #print(args)
        if args:
            films = [Films.objects.get(pk=args) for film in args]
        else:
            films = Films.objects.filter(kinopoisk_lastupdate = None,kinopoisk_id__isnull =False)[:LIMIT]

        for film in films:
            if film.kinopoisk_id is None:
                pass
            else:
                sleep(APP_FILM_CRAWLER_DELAY)
                try:
                    pdata = parse_one_page(film.kinopoisk_id)
                    a=[]
                    for d in pdata['Films']:
                        a.extend(d.items())
                    for key,value in dict(a).items():
                        setattr(film, key, value)

                    film.kinopoisk_lastupdate = datetime.datetime.now()
                    film.save()
                    for p in pdata['Persons']:
                        po = get_person(film,p['name'])

                        if 'photo' in p:
                            if not (po.photo or (p['photo'] is None)):
                                po.photo.save(os.path.join(APP_PERSON_PHOTO_DIR, str(po.id),'profile.jpg'),File(p['photo']))

                        if PersonsFilms.objects.filter(film=film,person=po):
                            pass
                        else:
                            pf = PersonsFilms(person = po , film = film, p_type = p['p_type'])
                            pf.save()

                    kpt = KinopoiskTries(film = film,try_time = datetime.datetime.now(),result = APP_ROBOT_SUCCESS )
                    kpt.save()

                except Exception, e:
                    print(e)
                    kpt = KinopoiskTries(film = film,try_time = datetime.datetime.now(),result = APP_ROBOT_FAIL )
                    kpt.save()
