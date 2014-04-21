#coding: utf-8
from django.contrib.auth.models import User

from apps.contents.constants import *
from apps.films.constants import *
from apps.contents.models import *
from apps.films.models import *

import factory
import datetime


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

    @factory.post_generation
    def countries(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for country in extracted:
                self.countries.add(country)


class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = User
    pk = factory.Sequence(lambda f: f)
    username = factory.Sequence(lambda q: u'name{0}'.format(q))
    password = factory.Sequence(lambda q: u'pass{0}'.format(q))


class ContentFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Contents
    pk = factory.Sequence(lambda o: o)
    name = factory.SelfAttribute('film.name')
    film = factory.SubFactory(FilmFactory)
    release_date = factory.SelfAttribute('film.release_date')
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
    name = factory.Sequence(lambda b: u'Жанр{0}'.format(b))
    description = factory.Sequence(lambda b: u'Описание Жанра_{0}'.format(b))


class PersonFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Persons
    pk = factory.Sequence(lambda u: u)
    name = factory.Sequence(lambda u: u'Персона{0}'.format(u))
    name_orig = factory.Sequence(lambda u: u'Person{0}'.format(u))
    bio = u'Биография'
    photo = u''


class PersonsFilmFactory(factory.DjangoModelFactory):
    FACTORY_FOR = PersonsFilms
    pk = factory.Sequence(lambda g: g)
    film = factory.SubFactory(FilmFactory)
    person = factory.SubFactory(PersonFactory)
    p_type = APP_PERSON_ACTOR


class CommentsFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Comments
    # pk = factory.Sequence(lambda x: x)
    user = factory.SubFactory(UserFactory)
    content = factory.SubFactory(ContentFactory)
    text = factory.Sequence(lambda x: u'Comment{0}'.format(x))


class FilmsExtrasFactory(factory.DjangoModelFactory):
    FACTORY_FOR = FilmExtras
    url = factory.Sequence(lambda v: u'http://www.poster.ru/{0}.jpeg'.format(v))
    pk = factory.Sequence(lambda v: v)
    film = factory.SubFactory(FilmFactory)
    type = APP_FILM_TYPE_ADDITIONAL_MATERIAL_POSTER
    name = factory.Sequence(lambda v: u'Постер{0}'.format(v))
    name_orig = factory.Sequence(lambda v: u'Poster{0}'.format(v))
    description = factory.Sequence(lambda v: u'Описание{0}'.format(v))


class CountriesFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Countries
    pk = factory.Sequence(lambda h: h)
    name = factory.Sequence(lambda h: u'Страна{0}'.format(h))
    name_orig = factory.Sequence(lambda h: u'Country{0}'.format(h))


class UsersFilmsFactory(factory.DjangoModelFactory):
    FACTORY_FOR = UsersFilms
    user = factory.SubFactory(UserFactory)
    film = factory.SubFactory(FilmFactory)
    status = APP_USERFILM_STATUS_UNDEF




