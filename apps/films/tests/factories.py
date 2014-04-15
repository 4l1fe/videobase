#coding: utf-8
__author__ = 'eugene'



import factory
from apps.films.models import Persons, PersonsFilms, Films
import datetime


class PersonFactory(factory.DjangoModelFactory):

    FACTORY_FOR = Persons
    name = u'Иван'
    name_orig = u'Ivan'
    bio = u'Иван иваныч'
    photo = ''
    id = 1


class FilmFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Films
    FACTORY_DJANGO_GET_OR_CREATE = ('name',)
    pk = factory.Sequence(lambda n: n)
    id = factory.Sequence(lambda n: n)
    name = factory.Sequence(lambda n: u'Фильм{0}'.format(n))
    type = u'FULL_FILM'
    release_date = datetime.date(2014, 3, 21)
    description = u'Боевик'
    name_orig = factory.Sequence(lambda n: u'Film{0}'.format(n))


class PersonsFilmography(factory.DjangoModelFactory):

    FACTORY_FOR = PersonsFilms
    film = factory.SubFactory(FilmFactory)
    person = factory.SubFactory(PersonFactory)
    p_type = ''

















