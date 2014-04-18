#coding: utf-8
__author__ = 'eugene'



import factory
from apps.films.models import Persons, PersonsFilms, Films, UsersPersons
from rest_framework.authtoken.models import Token
import datetime
from django.contrib.auth.models import User
import random



class PersonFactory(factory.DjangoModelFactory):

    FACTORY_FOR = Persons
    name = u'Nicolas Cage'
    name_orig = u'Nicolas Cage'
    bio = u''
    photo = ''
    id = 1
    pk = factory.Sequence(lambda n: n)


class FilmFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Films
    FACTORY_DJANGO_GET_OR_CREATE = ('name',)
    pk = factory.Sequence(lambda n: n)
    id = 1
    name = factory.Sequence(lambda n: u'Фильм{0}'.format(n))
    type = u'FULL_FILM'
    release_date = datetime.date(2014, 3, 21)
    description = u'Боевик'
    name_orig = factory.Sequence(lambda n: u'Film{0}'.format(n))


class PersonsFilmography(factory.DjangoModelFactory):

    FACTORY_FOR = PersonsFilms
    person = factory.SubFactory(PersonFactory)
    film = factory.SubFactory(FilmFactory)
    p_type = ''
    p_character = ''
    description = ''


class UsersPersonsFactory(factory.DjangoModelFactory):

    FACTORY_FOR = UsersPersons
    person = factory.SubFactory(PersonFactory)


class UserFactory(factory.DjangoModelFactory):

    FACTORY_FOR = User
    pk = factory.Sequence(lambda n: n)
    username = factory.Sequence(lambda n: u'admin{0}'.format(n))
    password = u'admin'























