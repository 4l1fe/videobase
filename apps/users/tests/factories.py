# coding: utf-8
from apps.users.models import User, UsersProfile, UsersPics

import factory
from factory.django import ImageField


class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = User
    username = factory.Sequence(lambda n: u'admin{0}'.format(n))
    password = u'admin'


class UserProfileFactory(factory.DjangoModelFactory):
    FACTORY_FOR = UsersProfile


class UserPicsFactory(factory.DjangoModelFactory):
    FACTORY_FOR = UsersPics
