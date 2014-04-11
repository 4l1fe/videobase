__author__ = 'eugene'


import factory
from apps.films.models import Persons


class PersonFactory(factory.Factory):

    FACTORY_FOR = Persons
    name = u'Серж'
    name_orig = u'Serj'
    bio = u'Сергей черепашка обожатель'
    photo = u'asdasd'
    id = 1
    extend = False

