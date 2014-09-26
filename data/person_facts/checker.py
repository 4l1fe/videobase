# coding: utf-8
from apps.films.models import Films, PersonsExtras
from apps.films.models import FilmExtras
from apps.films.constants import APP_FILM_TYPE_ADDITIONAL_MATERIAL_TRAILER

from apps.films.models import Countries

from data.checker import FactChecker
from data.constants import FLATLAND_NAME
from crawler.tasks.person_task import parse_kinopoisk_persons
from apps.films.models import Persons

person_checker = FactChecker(Persons)


def person_info_reload_corrector(person):
    if person.kinopoisk_id:
        parse_kinopoisk_persons.apply_async(
                     (
                        person.kinopoisk_id,
                     )
                )
        print u"Corrector updated person info successfully"


@person_checker.add("Person name is not in Russian")
def russian_name_check(person):
    #TODO
    pass


def person_poster_corrector(person):
    try:
        if person.photo.size < 2000:
            person.photo.delete()
        person.save()
        print u"Corrector removed person poster"
    except Exception, e:
        pass



@person_checker.add(u"Person has missing information", corrector=person_info_reload_corrector)
def person_check(person):
    name_check = True
    origin_name_check = True
    photo_check = True
    birthdate_check = True
    biography_check = True
    try:
        if not person.name_orig:
            print "Persone origin name is not set"
            origin_name_check = False
        if not person.name:
            print "Persone name is not set"
            name_check = False
        if not person.photo:
            print "Persone photo is not set"
            photo_check = False
        if not person.birthdate:
            print "Persone birthdate is not set"
            birthdate_check = False
        if not person.bio:
            print "Persone biography is not set"
            biography_check = False
    except:
        print u"Check for person", person.name, u"failed"

    if not origin_name_check or not name_check or not photo_check or not birthdate_check or not biography_check:
        return False
    else:
        return True

@person_checker.add(u"Person has incorrect poster size", corrector=person_poster_corrector)
def film_poster_size_check(person):
    try:
        if person.photo.size < 2000:
            return False
    except Exception, e:
        pass
    return True