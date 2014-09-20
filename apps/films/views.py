# coding: utf-8
import re
import os
import json
import warnings

from datetime import date, timedelta
from random import randrange
from cStringIO import StringIO
from PIL import Image, ImageEnhance

from django.core.files import File
from django.core.cache import cache
from django.core.context_processors import csrf
from django.core.serializers.json import DjangoJSONEncoder
from django.template import Context
from django.views.generic import View
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, redirect

from rest_framework import status

import apps.films.models as film_model
import apps.contents.models as content_model
from apps.films.api.serializers import vbFilm, vbComment, vbPerson
from apps.films.constants import APP_USERFILM_STATUS_PLAYLIST
from apps.films.api import SearchFilmsView

from utils.noderender import render_page
from utils.common import reindex_by


def get_new_namestring(namestring):
    m = re.match("(?P<pre>.+)v(?P<version>[0-9]+)[.]png", namestring)

    if m is None:
         filename = namestring + '_v1.png'
    else:
        d = m.groupdict()
        filename = '{:s}v{:d}.{:s}'.format(d['pre'], int(d['version']) + 1, 'png')

    return filename


def image_refresh(func):
    def wrapper(request):
        url = request.POST.get('image')
        m = re.match('.+[/]static[/]upload[/](?P<type>[^/]+)[/](?P<id>[0-9]+)', url)

        path = re.match('.+(?P<path>[/]static[/].+)', url)
        d = m.groupdict()

        if d['type'] == 'persons':
            p = film_model.Persons.objects.get(pk=int(d['id']))
        elif d['type'] == 'filmextras':
            p = film_model.FilmExtras.objects.get(pk=int(d['id']))
        else:
            warnings.warn("Unknown type {} of requests for image manipulation")

        im = Image.open('.' + path.groupdict()['path'])
        imc = func(d, im, request)

        imfile = StringIO()

        imc.save(imfile, "PNG")
        imfile.seek(0)

        p.photo.save(get_new_namestring(os.path.basename(path.groupdict()['path'])), File(imfile))
        return HttpResponse("OK")

    return wrapper


@image_refresh
def resize_image(d, im, request):
    x = int(request.POST.get('x'))
    y = int(request.POST.get('y'))
    x2 = int(request.POST.get('x2'))
    y2 = int(request.POST.get('y2'))
    imc = im.crop((x, y, x2, y2))

    return im


@image_refresh
def bri_con(d, im, request):
    br = request.POST.get('br')
    co = request.POST.get('co')
    bre = ImageEnhance.Brightness(im)

    imc = im
    if br:
        imc = bre.enhance(2*(int(br))/100.0)

    coe = ImageEnhance.Contrast(imc)
    if co:
        imc = coe.enhance(2*(int(co))/100.0)

    return imc


class IndexView(View):

    def get(self, *args, **kwargs):
        # Выбираем 4 новых фильма, у которых есть локации
        NEW_FILMS_CACHE_KEY = 'new_films'
        resp_dict_serialized = cache.get(NEW_FILMS_CACHE_KEY)
        # Расчитываем новинки, если их нет в кеше
        if resp_dict_serialized is None:
            o_film = film_model.Films.get_newest_films()

            # Фильмы показывались => ставим флаг просмотрено в true
            for film in o_film:
                film.was_shown = True
                film.save()

            # Сериализуем новинки и конвертируем результат в строку
            resp_dict_data = vbFilm(o_film, require_relation=False, extend=True, many=True).data
            resp_dict_serialized = json.dumps(resp_dict_data, cls=DjangoJSONEncoder)

            # Положим результат в кеш
            cache.set(NEW_FILMS_CACHE_KEY, resp_dict_serialized, 86400)

        else:
            resp_dict_data = json.loads(resp_dict_serialized)

        # Найдем relation для фильмов, если пользователь авторизован
        if self.request.user.is_authenticated():
            o_user = film_model.UsersFilms.objects.filter(
                user=self.request.user, film__in=[item['id'] for item in resp_dict_data]
            )
            o_user = reindex_by(o_user, 'film_id', True)

            for index, item in enumerate(resp_dict_data):
                if item['id'] in o_user:
                    resp_dict_data[index]['relation'] = o_user[item['id']].relation_for_vb_film

        # Топ комментариев к фильмам  пользователей
        comments = content_model.Comments.get_top_comments_with_rating(struct=True)

        # Выборка списка жанров из кеша, если есть
        genres_cache_key = film_model.Genres.get_cache_key()
        genres_data = cache.get(genres_cache_key)

        if genres_data is None:
            try:
                genres_data = list(film_model.Genres.get_grouped_genres())
                cache.set(genres_cache_key, genres_data, 86400)
            except:
                genres_data = []

        
        # Формируем ответ
        data = {
            'films_new': resp_dict_data,
            'filter_genres': genres_data,
            'comments': comments,
             # Список рекомендуемых фильмов
            'films': get_recommend_film(self.request),
        }

        return HttpResponse(render_page('index', data), status.HTTP_200_OK)


class PersonView(View):

    def get(self, *args, **kwargs):
        try:
            person = film_model.Persons.objects.get(pk=kwargs['resource_id'])
        except film_model.Persons.DoesNotExist:
            raise Http404

        vbp = vbPerson(person, extend=True)
        crutch = vbp.data  # костыль, до починки парсинга этих данных роботом.
        if not vbp.data['birthdate']:
            d1 = date(1960, 1, 1)
            d2 = date(1980, 12, 12)
            delta = d2 - d1
            delta = delta.days*24*60*60
            seconds = randrange(delta)
            birthdate = (d1 + timedelta(seconds=seconds))
            crutch['birthdate'] = birthdate.strftime('%d %B %Y')
            crutch['years_old'] = date.today().year - birthdate.year

        pfs = film_model.PersonsFilms.objects.filter(person=person)[:12]  # почему-то 12 первых фильмов. Был пагинатор
        vbf = vbFilm([pf.film for pf in pfs], many=True)
        crutch['filmography'] = vbf.data

        return HttpResponse(render_page('person', {'person': crutch}))


class FilmView(View):

    def get(self, *args, **kwargs):
        resp_dict, o_film = film_to_view(kwargs['film_id'])
        resp_dict['similar'] = calc_similar(o_film)

        # Trailer
        trailer = film_model.FilmExtras.get_trailer_by_film(kwargs['film_id'], first=True)
        if not trailer is None:
            resp_dict['trailer'] = trailer.url

        return HttpResponse(render_page('film', {'film': resp_dict}))


class PlayListView(View):

    def get(self, *args, **kwargs):
        film_id = kwargs.get('film_id', 1)
        if self.request.user.is_authenticated():
            # Init data
            film_data = {}
            playlist = {'id': 0}
            film_id = int(film_id)

            # Выборка плейлиста
            playlist_data = film_model.Films.objects.\
                filter(uf_films_rel__user=self.request.user.id, uf_films_rel__status=APP_USERFILM_STATUS_PLAYLIST).\
                order_by('uf_films_rel__created')

            # Обработка плейлиста
            len_playlist = len(playlist_data)
            if len_playlist > 0:
                if film_id > len(playlist_data) or film_id < 1:
                    return redirect('playlist_film_view', film_id=1)

                def arrow_data(data, f_id):
                    return {'id': f_id, 'name': data.name}

                if film_id < len(playlist_data):
                    playlist['next'] = arrow_data(playlist_data[film_id], film_id+1)

                if film_id > 1:
                    playlist['previous'] = arrow_data(playlist_data[film_id-2], film_id-1)

                film = playlist_data[film_id-1]
                film_data, o_film = film_to_view(film.id)

            # Update playlist
            playlist.update({
                'id': film_id,
                'film': film_data,
                'total_cnt': len_playlist,
                'items': vbFilm(playlist_data, many=True).data,

                # Список рекомендуемых фильмов
                'films': get_recommend_film(self.request),
            })

            return HttpResponse(render_page('playlist', {'playlist': playlist, 'film': film_data}))

        return redirect('login_view')


class SearchView(View):

    def get(self, *args, **kwargs):
        # Устанавливаем ответ по умолчанию и вызываем сериализатор поиска
        resp_dict = {
            'films': [],
        }

        if self.request.REQUEST.get('text'):
            try:
                resp_dict['films'] = SearchFilmsView.as_view()(self.request, use_thread=True).data
                resp_dict['search_text'] = self.request.REQUEST.get('text')
            except Exception, e:
                pass

        return HttpResponse(render_page('search', resp_dict))



def test_view(request):
    c = Context({})
    c.update(csrf(request))

    return render_to_response('api_test.html', c)


def calc_actors(o_film):
    filter = {
        'filter': {'pf_persons_rel__film': o_film.pk},
        'offset': 0,
        'limit': 5,
    }

    result = []
    try:
        result = list(film_model.Persons.get_sorted_persons_by_name(**filter).values('id', 'name'))
    except Exception, e:
        print "Caught exception {} in calc_actors".format(e)

    return result


def calc_similar(o_film):
    result = []
    try:
        result = vbFilm(film_model.Films.similar_api(o_film), many=True).data
    except Exception, e:
        print "Caught exception {} in calc_similar".format(e)

    return result


def calc_comments(o_film):
    try:
        content = content_model.Contents.objects.get(film=o_film.pk)
    except Exception, e:
        return []

    result_list = content_model.Comments.objects.filter(content=content.id).order_by('-created')[:5]
    try:
        result_list = vbComment(result_list, many=True).data
    except:
        result_list = []

    return result_list


def film_to_view(film_id):
    o_film = film_model.Films.objects.filter(pk=film_id).prefetch_related('genres', 'countries')

    if not len(o_film):
        raise Http404

    o_film = o_film[0]
    resp_dict = vbFilm(o_film, extend=True)

    try:
        resp_dict = resp_dict.data
    except Exception, e:
        raise Http404

    resp_dict['actors'] = calc_actors(o_film)
    resp_dict['comments'] = calc_comments(o_film)

    return resp_dict, o_film


def kinopoisk_view(request, film_id, *args, **kwargs):
    # Проверяем, есть ли иакой film_id в нашей базе данных
    # и что эта запись уникальна
    try:
        o_film = film_model.Films.objects.get(kinopoisk_id=film_id)
        return redirect('film_view', film_id=o_film.id)
    except Exception, e:
        pass

    return redirect('index_view')


def get_recommend_film(request):
    try:
        o_recommend = SearchFilmsView.as_view()(request, use_thread=True, recommend=True).data
        o_recommend = o_recommend['items']
    except Exception, e:
        o_recommend = []

    return o_recommend
