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
from apps.films.constants import APP_PERSON_ACTOR, APP_PERSON_DIRECTOR, APP_FILM_TYPE_ADDITIONAL_MATERIAL_POSTER, \
    APP_FILMS_EXTRAS_POSTER_HOST, APP_FILM_TYPE_ADDITIONAL_MATERIAL_TRAILER, APP_PERSON_SCRIPTWRITER


TWITTER_MESSAGE_TEMPLATE = u"Новый #{ftype} {f_name} {genres_string} {f_rating}/10, {f_year} http://vsevi.ru/films/{film_id}/"
CONTENT_TYPE = 'application/rss+xml; charset=utf-8'


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
        messages.append((film.name, film.id,
                         TWITTER_MESSAGE_TEMPLATE.format(
                             ftype=ftype,
                             f_name=film.name,
                             genres_string=genres_string,
                             f_rating=film.rating_cons,
                             f_year=film.release_date.year,
                             film_id=film.id
                         )
        ))

    result = {
        'messages': messages,
        'date': get_format_time(),
        'newdate': ''
    }

    return render(request, 'rss/tw_feed.html', result, content_type=CONTENT_TYPE)


def get_feed_vk(request):
    result = {
        'films': get_film_description(is_vk=True),
        'newdate': '',
        'date': get_format_time(),
    }

    return render(request, 'rss/vk_feed.html', result, content_type=CONTENT_TYPE)


def get_feed(request):
    result = {
        'films': get_film_description(big_poster=False),
        'newdate': '',
        'date': get_format_time(),
    }

    return render(request, 'rss/feed.html', result, content_type=CONTENT_TYPE)


def get_feed_fb(request):
    result = {
        'films': get_film_description(),
        'newdate': '',
        'date': get_format_time(),
    }

    return render(request, 'rss/fb_feed.html', result, content_type=CONTENT_TYPE)


def get_feed_comment(request):
    result = {
        'comments': get_comment(),
        'date': get_format_time()
    }
    return render(request, 'rss/comment_feed.html', result, content_type=CONTENT_TYPE)


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

    return zip(list_films, list_actor, list_director, list_poster, list_trailer, list_scriptwriter, list_cost, list_genres)


def get_price(film):
    cont_id_list = Contents.objects.filter(film=film.id).values_list('id', flat=True)
    locations = Locations.objects.filter(content__in=cont_id_list)
    price = -1
    cost = u'бесплатно'
    min_price = locations[0].price

    for location in locations:
        if min_price > location.price:
            price = min_price
            min_price = location.price

    if min_price != 0:
        cost = u'от {cost} рублей без рекламы'.format(cost=int(min_price))

    elif min_price == 0 and price != -1:
        cost = u'бесплатно или от {cost} рублей без рекламы'.format(cost=int(price))

    return cost


def get_extras(film, is_vk=False, big_poster=True):
    poster = u''
    trailer = u'http://vsevi.ru/film/{0}/'.format(film.id)
    film_extras = FilmExtras.objects.filter(film_id=film.id).all()

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


def get_comment():
    comments = Comments.get_comments_sorting_by_created()
    list_title = []
    list_date = []
    list_link = []
    list_description = []
    for comment in comments:
        list_title.append(comment.user.username)
        list_date.append(comment.created.strftime('%Y-%m-%d %H:%M'))
        list_link.append('http://vsevi.ru/films/' + str(comment.content.film_id))
        list_description.append(comment.text)

    return zip(list_title, list_date, list_link, list_description)
