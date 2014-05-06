#coding: utf-8

from django.contrib.auth.models import User

from apps.contents.models import Contents
from apps.films.models import Persons, PersonsFilms, Films, UsersPersons, PersonsExtras, Cities, Countries

import datetime
import factory


class PersonFactory(factory.DjangoModelFactory):

    FACTORY_FOR = Persons
    name = u'Nicolas Cage'
    name_orig = u'Nicolas Cage'
    bio = u''
    photo = ''
    city = factory.SubFactory('apps.films.tests.factories.CitiesFactory')
    birthdate = datetime.date.today()
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
    p_type = ''  # TODO: не строкой , а вариантом из значений поля модели
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


class PersonsExtrasFactory(factory.DjangoModelFactory):
    FACTORY_FOR = PersonsExtras
    person = factory.SubFactory(PersonFactory)
    name        = u'Имя'
    name_orig   = u'Оригинальное имя'
    description = u'Описание'
    pk = factory.Sequence(lambda n: n)


class CitiesFactory(factory.DjangoModelFactory):

    FACTORY_FOR = Cities
    country = factory.SubFactory('apps.films.tests.factories.CountriesFactory')
    name = u'factory_city'
    name_orig = u'factory_city_orig'
    pk = factory.Sequence(lambda n: n)


class CountriesFactory(factory.DjangoModelFactory):

    FACTORY_FOR = Countries
    name = u'factory_country'
    name_orig = u'factory_country_orig'
    description = u''
    pk = factory.Sequence(lambda n: n)
