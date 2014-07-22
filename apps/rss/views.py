# coding: utf-8

import time
from email import utils

from django.shortcuts import render
from django.utils.timezone import datetime

from apps.contents.models import Contents, Locations
from apps.films.models import Films, PersonsFilms, FilmExtras

from apps.films.constants import APP_PERSON_ACTOR, APP_PERSON_DIRECTOR, APP_FILM_TYPE_ADDITIONAL_MATERIAL_POSTER, \
    APP_FILMS_EXTRAS_POSTER_HOST, APP_FILM_TYPE_ADDITIONAL_MATERIAL_TRAILER, APP_PERSON_SCRIPTWRITER

TWITTER_MESSAGE_TEMPLATE = u"Новый #{ftype} {f_name} {genres_string} {f_rating}/10, {f_year} http://vsevi.ru/films/{film_id}/"


def get_format_time():
    current_timestamp = time.mktime(datetime.now().timetuple())

    return utils.formatdate(current_timestamp)


def get_feed_tw(request):
    messages = []
    for film in Films.get_newest_films():
        genres = list(get_genres(film))

        ftype = u'фильм'
        if u'мультфильм' in genres:
            ftype = u'мультфильм'
            genres.remove(ftype)

        genres_string = u'#{0}'.format(u' #'.join(genres))
        messages.append((film.name, film.id, TWITTER_MESSAGE_TEMPLATE.format(ftype=ftype,
                                                         f_name=film.name,
                                                         genres_string=genres_string,
                                                         f_rating=film.rating_cons,
                                                         f_year=film.release_date.year,
                                                         film_id=film.id)))
    result = {
        'messages': messages,
        'date': get_format_time(),
        'newdate': ''
    }

    return render(request, 'tw_feed.html', result,
                  content_type='application/rss+xml; charset=utf-8')


def get_feed_vk(request):
    result = {
        'films': get_film_description(is_vk=True),
        'newdate': '',
        'date': get_format_time(),
    }

    return render(request, 'vk_feed.html', result,
                  content_type='application/rss+xml; charset=utf-8')


def get_feed(request):
    result = {
        'films': get_film_description(big_poster=False),
        'newdate': '',
        'date': get_format_time(),
    }

    return render(request, 'feed.html', result,
                  content_type='application/rss+xml; charset=utf-8')


def get_feed_fb(request):
    result = {
        'films': get_film_description(),
        'newdate': '',
        'date': get_format_time(),
    }

    return render(request, 'fb_feed.html', result,
                  content_type='application/rss+xml; charset=utf-8')


def get_film_description(**kwargs):
    list_cost = []
    list_genres = []
    list_poster = []
    list_trailer = []
    list_actor = []
    list_director = []
    list_scriptwriter = []
    films = Films.get_newest_films()

    for film in films:
        cost = get_price(film)
        genres = get_genres(film)
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

    return zip(films, list_actor, list_director, list_poster, list_trailer, list_scriptwriter, list_cost, list_genres)


def get_price(film):
    locations = Locations.objects.filter(content__in=Contents.objects.filter(film=film.id).values_list('id', flat=True))
    min_price = locations[0].price

    price = -1
    cost = u'бесплатно'

    for location in locations:
        if min_price > location.price:
            price = min_price
            min_price = location.price

    if min_price != 0:
        cost = u'от {0} рублей без рекламы'.format(min_price)

    elif min_price == 0 and price != -1:
        cost = u'бесплатно или от {0} рублей без рекламы'.format(price)

    return cost


def get_extras(film, is_vk=False, big_poster=True):
    film_extras = FilmExtras.objects.filter(film_id=film.id).all()
    poster = u''
    trailer = u'http://vsevi.ru/film/{0}/'.format(film.id)

    for extras in film_extras:
        if is_vk:
            if extras.type == APP_FILM_TYPE_ADDITIONAL_MATERIAL_TRAILER:
                trailer = extras.url

        if extras.type == APP_FILM_TYPE_ADDITIONAL_MATERIAL_POSTER:
            poster = extras.photo.url if big_poster else extras.get_photo_url(prefix=True)

            if len(poster):
                poster = u"http://vsevi.ru{0}".format(poster)

    return poster, trailer


def get_genres(film):
    return film.genres.all().values_list('name', flat=True)


def get_person(film):
    cnt_actor = 0
    list_actor_by_film = []
    list_director_by_film = []
    list_scriptwriter_by_film = []

    persons = PersonsFilms.objects.filter(film_id=film.id).all()

    for person in persons:
        if person.p_type == APP_PERSON_ACTOR and cnt_actor < 6:
            cnt_actor += 1
            list_actor_by_film.append(person.person.name)

        elif person.p_type == APP_PERSON_DIRECTOR:
            list_director_by_film.append(person.person.name)

        elif person.p_type == APP_PERSON_SCRIPTWRITER:
            list_scriptwriter_by_film.append(person.person.name)

    return u', '.join(list_actor_by_film), u', '.join(list_director_by_film), u', '.join(list_scriptwriter_by_film)
