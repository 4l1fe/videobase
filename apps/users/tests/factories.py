# coding: utf-8
from apps.users.models import User, UsersProfile

import factory


class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = User
    pk = factory.Sequence(lambda n: n)
    username = factory.Sequence(lambda n: u'admin{0}'.format(n))
    password = u'admin'


class UserProfileFactory(factory.DjangoModelFactory):
    FACTORY_FOR = UsersProfile
    pk = factory.Sequence(lambda n: n)
