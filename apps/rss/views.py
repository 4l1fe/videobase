# coding: utf-8

import time
import json
from email import utils

from django.shortcuts import render
from django.utils.timezone import datetime
from django.core.serializers.json import DjangoJSONEncoder
from django.core.cache import cache

from apps.contents.models import Contents, Locations, Comments

from apps.films.models import Films, PersonsFilms, FilmExtras
from apps.films.api.serializers import vbFilm
from apps.films.constants import APP_PERSON_ACTOR, APP_PERSON_DIRECTOR,\
    APP_FILM_TYPE_ADDITIONAL_MATERIAL_POSTER,\
    APP_FILM_TYPE_ADDITIONAL_MATERIAL_TRAILER, APP_PERSON_SCRIPTWRITER, \
    APP_FILM_TYPE_FILM, APP_FILM_TYPE_ANIMATED_FILM

CONTENT_TYPE = 'application/rss+xml; charset=utf-8'


def get_format_time():
    current_timestamp = time.mktime(datetime.now().timetuple())
    return utils.formatdate(current_timestamp)


def feed_view(request, social):
    feed_map = {
        # feed rss
        None: (get_film_description, {"big_poster": False, "trailer": True}),
        # twitter rss
        '_tw': (get_feed_tw, {}),
        # facebook rss
        '_fb': (get_film_description, {}),
        # comments rss
        '_comment': (get_feed_comment, {}),
        # vk.com rss
        '_vk': (get_film_description, {'trailer': True}),
        # odnoklassniki rss
        '_ok': (get_film_description, {'trailer': True}),
    }

    context = {'date': get_format_time()}
    data_function, kwargs = feed_map.get(social)
    context.update({'description': data_function(**kwargs)})
    return render(request, 'rss/feed{0}.html'.format(social or ''), context, content_type=CONTENT_TYPE)


def get_feed_tw():
    films = []
    for film in Films.get_newest_films():
        genres = list(film.genres.all().values_list('name', flat=True))[0:2]
        film.film_type = get_film_type(genres)
        films.append((film, genres))
    return films


def get_feed_comment():
    comments = Comments.get_comments_sorting_by_created()
    return comments


def get_film_type(genres):
    film_type = APP_FILM_TYPE_FILM
    if APP_FILM_TYPE_ANIMATED_FILM in genres:
        film_type = APP_FILM_TYPE_ANIMATED_FILM
        genres.remove(APP_FILM_TYPE_ANIMATED_FILM)
    return film_type


def get_film_description(**kwargs):
    NEW_FILMS_CACHE_KEY = 'new_films'
    cached_films = cache.get(NEW_FILMS_CACHE_KEY)

    # Расчитываем новинки, если их нет в кеше
    if cached_films is None:
        films = Films.get_newest_films()

        for film in films:
            # Фильмы показывались => ставим флаг просмотрено в true
            film.was_shown = True
            film.save()

        # Сериализуем новинки и конвертируем результат в строку
        dict_data = vbFilm(films, require_relation=False, extend=True, many=True).data
        json_dict_serialized = json.dumps(dict_data, cls=DjangoJSONEncoder)

        # Положим результат в кеш
        cache.set(NEW_FILMS_CACHE_KEY, json_dict_serialized, 86400)

    else:
        dict_data = json.loads(cached_films)

    list_cost = []
    list_genres = []
    list_poster = []
    list_trailer = []
    list_actor = []
    list_director = []
    list_scriptwriter = []
    list_films = []

    for index, item in enumerate(dict_data):
        film = Films.objects.get(id=item['id'])
        list_films.append(film)
        cost = get_price(film)
        genres = list(film.genres.all().values_list('name', flat=True))
        film.film_type = get_film_type(genres)
        poster, trailer = get_extras(film, **kwargs)
        list_persons_by_film = get_person(film)

        # Add Cost and genres
        list_cost.append(cost)
        list_genres.append(genres)

        # Add persons
        list_actor.append(list_persons_by_film[0])
        list_director.append(list_persons_by_film[1])
        list_scriptwriter.append(list_persons_by_film[2])

        # Add poster and trailer
        list_poster.append(poster)
        list_trailer.append(trailer)

    return zip(list_films, list_actor, list_director, list_poster, list_trailer, list_scriptwriter, list_cost, list_genres)


def get_price(film):
    cont_id_list = Contents.objects.filter(film=film.id).values_list('id', flat=True)
    locations = Locations.objects.filter(content__in=cont_id_list).order_by('price')
    result = []
    min_location = min(locations, key=lambda loc: loc.price)
    result.append(min_location)
    if min_location.price == 0:
        locations_qt = filter(lambda loc: loc.price > 0, locations)
        if locations_qt:
            result.append(locations_qt[0])
    return result


def get_extras(film, trailer=False, big_poster=True):
    poster = u''
    trailer_url = u'http://vsevi.ru/film/{0}/'.format(film.id)
    film_extras = FilmExtras.objects.filter(film_id=film.id).all()

    for extras in film_extras:
        if trailer and extras.type == APP_FILM_TYPE_ADDITIONAL_MATERIAL_TRAILER:
            trailer_url = extras.url

        if extras.type == APP_FILM_TYPE_ADDITIONAL_MATERIAL_POSTER:
            poster = extras.photo.url if big_poster else extras.get_photo_url(prefix=True)

            if poster:
                poster = u"http://vsevi.ru{0}".format(poster)

    return poster, trailer_url


def get_person(film):
    list_actor_by_film = []
    list_director_by_film = []
    list_scriptwriter_by_film = []

    persons = PersonsFilms.objects.filter(film_id=film.id).all()

    for person in persons:
        if person.p_type == APP_PERSON_ACTOR and len(list_actor_by_film) < 6:
            list_actor_by_film.append(person.person)

        elif person.p_type == APP_PERSON_DIRECTOR:
            list_director_by_film.append(person.person)

        elif person.p_type == APP_PERSON_SCRIPTWRITER:
            list_scriptwriter_by_film.append(person.person)

    return list_actor_by_film, list_director_by_film, list_scriptwriter_by_film

