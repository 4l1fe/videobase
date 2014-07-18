# coding: utf-8

from django.shortcuts import render, HttpResponse
from django.utils.timezone import datetime
from apps.contents.models import Contents, Locations
from apps.films.constants import APP_PERSON_ACTOR, APP_PERSON_DIRECTOR, APP_FILM_TYPE_ADDITIONAL_MATERIAL_POSTER, \
    APP_FILMS_EXTRAS_POSTER_HOST, APP_FILM_TYPE_ADDITIONAL_MATERIAL_TRAILER
from apps.films.models import Films, PersonsFilms, FilmExtras
import copy
import time
from email import utils
TWITTER_MESSAGE_TEMPLATE = u"Новый #{ftype} {f_name} {genres_string} {f_rating}/10, {f_year} http://vsevi.ru/films/{film_id}"


def get_format_time():
    nowdt = datetime.now()
    nowtuple = nowdt.timetuple()
    nowtimestamp = time.mktime(nowtuple)
    return utils.formatdate(nowtimestamp)

def get_feed_tw(request):
    films = Films.get_newest_films()
    #films = Films.objects.all()[:4]
    messages = []
    for film in films:
        genres = [genre.name for genre in film.genres.all()]
        if u'мультфильм' in genres:
            ftype = u'мультфильм'
            genres.remove(u'мультфильм')
        else:
            ftype = u'фильм'

        genres_string = '#'+' #'.join(genres)
        messages.append( (film.name,film.id,TWITTER_MESSAGE_TEMPLATE.format(ftype=ftype,
                                                         f_name=film.name,
                                                         genres_string=genres_string,
                                                         f_rating=film.rating_cons,
                                                         f_year=film.release_date.year,
                                                         film_id=film.id)))
    result = {'messages': messages, 'date': get_format_time(), 'newdate': ''}
        
    return HttpResponse(render(request, 'tw_feed.html',
                  result), content_type="application/rss+xml ; charset=utf-8")


def get_feed_vk(request):
    result = {'films': get_film_description(True), 'newdate': '', 'date': get_format_time()}
    return HttpResponse(render(request, 'vk_feed.html',
                  result), content_type="application/rss+xml ; charset=utf-8")


def get_feed(request):
    result = {'films': get_film_description(False), 'newdate': '', 'date': get_format_time()}
    return HttpResponse(render(request, 'feed.html',
                  result), content_type="application/rss+xml ; charset=utf-8")


def get_feed_fb(request):
    result = {'films': get_film_description(False), 'newdate': '', 'date': get_format_time()}
    return HttpResponse(render(request, 'fb_feed.html',
                  result), content_type="application/rss+xml ; charset=utf-8")


def get_film_description(is_vk):
    list_actor = []
    list_director = []
    list_poster = []
    list_trailer = []
    list_scriptwriter = []
    list_cost = []
    films = Films.get_newest_films()

    for film in films:
        poster, trailer = get_extras(film, is_vk)

        list_actor_by_film, list_director_by_film, list_scriptwriter_by_film = get_person(film)
        cost = get_price(film)
        list_cost.append(copy.deepcopy(cost))
        list_cost.append(cost)
        list_director.append(copy.deepcopy(list_director_by_film))
        list_actor.append(copy.deepcopy(list_actor_by_film))
        list_poster.append(copy.deepcopy(poster))
        list_trailer.append(copy.deepcopy(trailer))
        list_scriptwriter.append(copy.deepcopy(list_scriptwriter_by_film))

    return zip(films, list_actor, list_director, list_poster, list_trailer, list_scriptwriter, list_cost)


def get_price(film):
    content = Contents.objects.get(film=film.id)
    locations = Locations.objects.filter(content=content.id)
    min_price = locations[0].price
    price = -1
    cost = u'бесплатно'
    for location in locations:
        if min_price > location.price:
            price = min_price
            min_price = location.price

    if min_price != 0:
        cost = u'от ' + str(int(min_price)) + u' рублей без рекламы'

    if min_price == 0 and price != -1:
        cost = u'бесплатно или от ' + str(int(price)) + u' рублей без рекламы'

    return cost


def get_extras(film, is_vk):
    film_extras = FilmExtras.objects.filter(film_id=film.id).all()
    poster = ''
    trailer = 'http://vsevi.ru/film/{0}/'.format(film.id)

    for extras in film_extras:

        if extras.type == APP_FILM_TYPE_ADDITIONAL_MATERIAL_POSTER:
            poster = APP_FILMS_EXTRAS_POSTER_HOST + extras.photo.name

        if is_vk:
            if extras.type == APP_FILM_TYPE_ADDITIONAL_MATERIAL_TRAILER:
                trailer = extras.url

    return poster, trailer


def get_person(film):
    list_actor_by_film = []
    list_director_by_film = []
    list_scriptwriter_by_film = []
    cnt_actor = 0
    persons = PersonsFilms.objects.filter(film_id=film.id).all()

    for person in persons:

        if person.p_type == APP_PERSON_ACTOR and cnt_actor < 6:
            cnt_actor += 1
            list_actor_by_film.append(person.person.name)

        elif person.p_type == APP_PERSON_DIRECTOR:
            list_director_by_film.append(person.person.name)
        else:
            list_scriptwriter_by_film.append(person.person.name)

    return ', '.join(list_actor_by_film), ', '.join(list_director_by_film), ', '.join(list_scriptwriter_by_film)

