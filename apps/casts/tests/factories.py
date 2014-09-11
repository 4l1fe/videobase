# coding: utf-8

import factory
from django.utils import timezone

from apps.films.tests.factories import FilmsExtrasFactory, UserFactory
from apps.casts.models import Casts, AbstractCastsTags, CastsExtras, UsersCasts, CastsChatsMsgs, CastsChats


class CastsFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Casts
    FACTORY_DJANGO_GET_OR_CREATE = ('title',)
    title       = u'Футбол'
    title_orig  = u'Football'
    start       = timezone.now()
    duration    = 60
    status      = 'on'
    description = 'Ukraine - Mexico'
    pg_rating   = 18

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for tag in extracted:
                self.tags.add(tag)


class TagFactory(factory.DjangoModelFactory):
    FACTORY_FOR = AbstractCastsTags
    name        = 'Имя тега'
    name_orig   = 'Tag Name'
    description = 'Tag description'


class CastsExtrasFactory(factory.DjangoModelFactory):
    FACTORY_FOR = CastsExtras
    cast        = factory.SubFactory(CastsFactory)
    extra       = factory.SubFactory(FilmsExtrasFactory)


class UserCastsFactory(factory.DjangoModelFactory):
    FACTORY_FOR = UsersCasts
    user        = factory.SubFactory(UserFactory)
    cast        = factory.SubFactory(CastsFactory)
    subscribed  = timezone.now()
    rating      = 1


class CastsChatFactory(factory.DjangoModelFactory):
    FACTORY_FOR = CastsChats
    cast        = factory.SubFactory(CastsFactory)
    status      = 1

    class Meta:
        django_get_or_create = ('cast',)


class CastsChatsMsgsFactory(factory.DjangoModelFactory):
    FACTORY_FOR = CastsChatsMsgs
    cast        = factory.SubFactory(CastsFactory)
    created     = timezone.now()
    user        = factory.SubFactory(UserFactory)
    text        = "Factory generated text"
