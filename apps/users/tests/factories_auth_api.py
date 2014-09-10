#coding: utf-8
from django.contrib.auth.models import User

import factory


class UserFactory(factory.DjangoModelFactory):

    FACTORY_FOR = User
    pk = factory.Sequence(lambda n: n)
    username = u'admin'
    password = u'admin'
