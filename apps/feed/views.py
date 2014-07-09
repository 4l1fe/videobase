from django.shortcuts import render
from datetime import datetime
from apps.films.constants import APP_PERSON_ACTOR, APP_PERSON_DIRECTOR, APP_FILM_TYPE_ADDITIONAL_MATERIAL_POSTER, \
    APP_FILMS_EXTRAS_POSTER_HOST, APP_FILM_TYPE_ADDITIONAL_MATERIAL_TRAILER
from apps.films.models import Films, PersonsFilms, FilmExtras
import copy


def get_feed_tw(request):
    films = Films.get_newest_films().all()
    result = {'films': films, 'date': datetime.utcnow(), 'newdate': ''}
    return render(request, 'tw_feed.html',
                  result)


def get_feed_vk(request):
    result = {'films': get_film_descriprion(True), 'newdate': '', 'date': datetime.utcnow()}
    return render(request, 'vk_feed.html',
                  result)


def get_feed(request):
    films = Films.get_newest_films().all()
    result = {'films': films, 'newdate': '', 'date': datetime.utcnow()}
    return render(request, 'feed.html',
                  result)


def get_feed_fb(request):
    result = {'films': get_film_descriprion(False), 'newdate': '', 'date': datetime.utcnow() }
    return render(request, 'fb_feed.html',
                  result)


def get_film_descriprion(is_vk):
    list_actor = []
    list_director = []
    list_poster = []
    list_trailer = []
    films = Films.get_newest_films().all()

    for film in films:
        list_actor_by_film = []
        list_director_by_film = []
        list_poster_by_film = []
        list_trailer_by_film = []
        cnt_actor = 0
        persons = PersonsFilms.objects.filter(film_id=film.id).all()
        film_extras = FilmExtras.objects.filter(film_id=film.id).all()
        trailer = 'http://vsevi.ru/films/' + str(film.id)
        for extras in film_extras:

            if extras.type == APP_FILM_TYPE_ADDITIONAL_MATERIAL_POSTER:
                poster = APP_FILMS_EXTRAS_POSTER_HOST + extras.photo.name
                list_poster_by_film.append(poster)
            if is_vk:
                if extras.type == APP_FILM_TYPE_ADDITIONAL_MATERIAL_TRAILER:
                    trailer = extras.url
                    break

        list_trailer_by_film.append(trailer)

        for person in persons:

            if person.p_type == APP_PERSON_ACTOR and cnt_actor < 6:
                cnt_actor += 1
                list_actor_by_film.append(person.person.name)

            elif person.p_type == APP_PERSON_DIRECTOR:
                list_director_by_film.append(person.person.name)

        list_director.append(copy.deepcopy(list_director_by_film))
        list_actor.append(copy.deepcopy(list_actor_by_film))
        list_poster.append(copy.deepcopy(list_poster_by_film))
        list_trailer.append(copy.deepcopy(list_trailer_by_film))
    return zip(films, list_actor, list_director, list_poster, list_trailer)