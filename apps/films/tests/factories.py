#coding: utf-8
__author__ = 'eugene'

import factory
from apps.films.models import Persons, Films


class PersonFactory(factory.DjangoModelFactory):

    FACTORY_FOR = Persons
    name = u'Серж'
    name_orig = u'Serj'
    bio = u'Сергей черепашка обожатель'
    photo = u'asdasd'
    id = 1
    pk = 1


class FilmFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Films
    pk = 1
    id = 1
    name = u'РЭД'
    type = u'FULL_FILM'
    release_date = u'2014-03-21'
    description = u'Боевик'
    name_orig = u'RED'
