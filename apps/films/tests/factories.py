#coding: utf-8
from apps.contents.constants import APP_CONTENTS_ONLINE_CINEMA, APP_CONTENTS_PRICE_TYPE_FREE

__author__ = 'eugene'

import factory
import datetime
from apps.contents.models import Contents, Locations
from apps.films.models import Persons, Films, Genres


class FilmFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Films
    FACTORY_DJANGO_GET_OR_CREATE = ('name',)
    pk = factory.Sequence(lambda n: n)
    name = factory.Sequence(lambda n: u'Фильм{0}'.format(n))
    type = u'FULL_FILM'
    release_date = datetime.date(2014, 3, 21)
    description = u'Боевик'
    name_orig = factory.Sequence(lambda n: u'Film{0}'.format(n))
    @factory.post_generation
    def genres(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for genre in extracted:
                self.genres.add(genre)



class ContentFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Contents
    pk = factory.Sequence(lambda o: o)
    name = factory.SelfAttribute('film.name')
    film = factory.SubFactory(FilmFactory)
    release_date =factory.SelfAttribute('film.release_date')
    viewer_cnt = 0
    viewer_lastweek_cnt = 0
    viewer_lastmonth_cnt = 0


class LocationFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Locations
    pk = factory.Sequence(lambda m: m)
    content = factory.SubFactory(ContentFactory)
    type = APP_CONTENTS_ONLINE_CINEMA
    lang = u'eng'
    price = float(0)
    price_type = APP_CONTENTS_PRICE_TYPE_FREE
    url_view = u'http://www.megogo.net/item/Red.html'
    quality = u''
    subtitles = u''


class GenreFactory(factory.DjangoModelFactory):
    pk = factory.Sequence(lambda b: b)
    FACTORY_FOR = Genres
    name = factory.Sequence(lambda c: u'Жанр{0}'.format(c))
    description = factory.Sequence(lambda a: u'Описание Жанра_{0}'.format(a))







