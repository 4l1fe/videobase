# coding: utf-8
from django.core.files import File

from crawler.datarobots.kinopoisk_ru.parse_page import get_poster, get_small_poster
from apps.films.models import FilmExtras, Films
from apps.films.constants import APP_FILM_TYPE_ADDITIONAL_MATERIAL_POSTER


def set_kinopoisk_poster(film):
    poster = get_poster(film.kinopoisk_id)
    if not poster:
        poster = get_small_poster(film.kinopoisk_id)
    if poster:
        print u"Adding poster for {}".format(film)
        fe = FilmExtras(film=film, type=APP_FILM_TYPE_ADDITIONAL_MATERIAL_POSTER, name=u"Постер для {}".format(film.name),
                        name_orig=u"Poster for {}".format(film.name), description=" ")
        fe.save()
        print u"Created film extras {}".format(fe.pk)
        fe.photo.save('poster.jpg', File(poster))


def poster_robot_wrapper(film_id):
    try:
        film = Films.objects.get(pk = film_id)
        if film.kinopoisk_id:
            set_kinopoisk_poster(film)
        else:
            print "Kinopoisk id not defined for {}".format(film)
    except Films.DoesNotExist:
        print "Couldn't find that film"
