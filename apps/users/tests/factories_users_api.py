# coding: utf-8
import datetime
import factory
from factory.django import ImageField

from apps.users.models import User, UsersPics, UsersRels, Feed
from apps.contents.models import Comments, Contents, Locations
from apps.contents.constants import APP_CONTENTS_PRICE_TYPE_FREE
from apps.films.models import Films, Genres, UsersFilms, UsersPersons, Persons, Countries, Cities, PersonsFilms
from apps.films.constants import APP_FILM_FULL_FILM
from apps.contents.constants import APP_CONTENTS_LOC_TYPE


class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = User
    username = factory.Sequence(lambda n: u'admin{0}'.format(n))
    password = u'admin'


class FeedFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Feed
    user = factory.SubFactory(UserFactory)


class UserRelsFactory(factory.DjangoModelFactory):
    FACTORY_FOR = UsersRels


class GenreFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Genres
    name = factory.Sequence(lambda i: u'Жанр{0}'.format(i))
    description = factory.Sequence(lambda b: u'Описание Жанра_{0}'.format(b))


class FilmFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Films
    FACTORY_DJANGO_GET_OR_CREATE = ('name',)
    kinopoisk_id = factory.Sequence(lambda i: i)
    name = factory.Sequence(lambda n: u'Фильм{0}'.format(n))
    type = APP_FILM_FULL_FILM
    release_date = datetime.datetime.now()

    @factory.post_generation
    def genres(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for genre in extracted:
                self.genres.add(genre)


class UserFilmsFactory(factory.DjangoModelFactory):
    FACTORY_FOR = UsersFilms
    film = factory.SubFactory(FilmFactory)


class ContetsFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Contents
    name = factory.SelfAttribute('film.name')
    film = factory.SubFactory(FilmFactory)
    release_date = factory.SelfAttribute('film.release_date')
    viewer_cnt = 0
    viewer_lastweek_cnt = 0
    viewer_lastmonth_cnt = 0


class LocationsFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Locations
    content = factory.SubFactory(ContetsFactory)
    type = APP_CONTENTS_LOC_TYPE[0][0]
    lang = u'eng'
    price = float(0)
    price_type = APP_CONTENTS_PRICE_TYPE_FREE
    url_view = u'http://www.megogo.net/item/Red.html'
    quality = u''
    subtitles = u''


class CommentsFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Comments
    content = factory.SubFactory(ContetsFactory)
    text = factory.Sequence(lambda i: u'Text{0}'.format(i))


class CountriesFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Countries
    name = factory.Sequence(lambda n: u'Имя_{0}'.format(n))
    name_orig = factory.Sequence(lambda n: u'ОригинальноеИмя_{0}'.format(n))
    description = factory.Sequence(lambda n: u'Описание_{0}'.format(n))


class CitiesFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Cities
    name = factory.Sequence(lambda n: u'Имя_{0}'.format(n))
    name_orig = factory.Sequence(lambda n: u'ОригинальноеИмя_{0}'.format(n))
    country = factory.SubFactory(CountriesFactory)


class PersonsFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Persons
    kinopoisk_id = factory.Sequence(lambda i: i)
    name = factory.Sequence(lambda n: u'Персона_{0}'.format(n))
    bio = factory.Sequence(lambda n: u'Биография_{0}'.format(n))
    photo = ImageField(color='red')
    birthdate = datetime.datetime.now()
    city = factory.SubFactory(CitiesFactory)


class PersonsFilmsFactory(factory.DjangoModelFactory):
    FACTORY_FOR = PersonsFilms
    film = factory.SubFactory(FilmFactory)
    person = factory.SubFactory(PersonsFactory)


class UserPersonsFatory(factory.DjangoModelFactory):
    FACTORY_FOR = UsersPersons
    person = factory.SubFactory(PersonsFactory)


class UserPicsFactory(factory.DjangoModelFactory):
    FACTORY_FOR = UsersPics
    image = ImageField(color='blue')
