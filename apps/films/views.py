# coding: utf-8

import re
import os
import warnings
from datetime import date, timedelta
from random import randrange
from cStringIO import StringIO
from PIL import Image, ImageEnhance

from django.core.files import File
from django.core.cache import cache
from django.core.context_processors import csrf

from django.template import Context
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.utils import timezone

from rest_framework import status

import apps.films.models as film_model
from apps.films.models import PersonsFilms
from apps.films.api.serializers import vbFilm, vbComment, vbPerson
from apps.films.api.serializers.vb_film import GenresSerializer
import apps.contents.models as content_model
from django.core.serializers.json import DjangoJSONEncoder
from utils.noderender import render_page


import json

# Do not remove there is something going on when importing, probably models registering itselves
# import apps.films.models

NEW_FILMS_CACHE_KEY = "new_films"

def get_new_namestring(namestring):

    m = re.match("(?P<pre>.+)v(?P<version>[0-9]+)[.]png", namestring)

    if m is None:
        return namestring + '_v1.png'
    else:
        d = m.groupdict()
        return '{:s}v{:d}.{:s}'.format(d['pre'], int(d['version']) + 1, 'png')

      
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


def index_view(request):
    resp_dict_serialized = cache.get(NEW_FILMS_CACHE_KEY)

    if resp_dict_serialized is None:
        encoder = DjangoJSONEncoder
        # Form 4 films that have locations and are newest and have release date less than now.
    
        o_locs = content_model.Locations.objects.all()
        o_film = sorted(set((ol.content.film for ol in o_locs if ol.content.film.release_date < timezone.now().date())),
                        key=lambda f: f.release_date)[-4:]

        resp_dict_data = vbFilm(o_film, extend=True, many=True).data
        resp_dict_serialized = json.dumps(resp_dict_data, cls=encoder)
        cache.set(NEW_FILMS_CACHE_KEY, resp_dict_serialized, 9000)

    else:
        resp_dict_data = json.loads(resp_dict_serialized)

    o_genres = GenresSerializer(film_model.Genres.objects.all(), many=True)

    data = {
        'new_films': resp_dict_data,
        'genres': [{'id': genre['id'],
                    'name': genre['name'],
                    'order': i} for i, genre in enumerate(sorted(o_genres.data, key=lambda g: g['name']))],
    }
    
    return HttpResponse(render_page('index', data), status.HTTP_200_OK)


def person_view(request, resource_id):
    try:
        person = film_model.Persons.objects.get(pk=resource_id)
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
    if not vbp.data.get('bio', None):
        crutch['bio'] = 'Заглушка для биографии, пока робот не починен'
    pfs = film_model.PersonsFilms.objects.filter(person=person)[:12]  # почему-то 12 первых фильмов. Был пагинатор
    vbf = vbFilm([pf.film for pf in pfs], many=True)

    return HttpResponse(render_page('person', {'person': crutch, 'filmography': vbf.data}))


def test_view(request):
    c = Context({})
    c.update(csrf(request))

    return render_to_response('api_test.html', c)


def calc_actors(o_film):
    result_list = []
    filter = {
        'filter': {'person_film_rel__film': o_film.pk},
        'offset': 0,
        'limit': 5,
    }

    try:
        result_list = list(film_model.Persons.get_sorted_persons_by_name(**filter).values('id', 'name'))
    except Exception, e:
        pass

    return result_list


def calc_similar(o_film):
    try:
        result = film_model.Films.similar_api(o_film)
        result = vbFilm(result).data
    except Exception, e:
        pass

    return result


def calc_comments(o_film):
    try:
        content = content_model.Contents.objects.get(film=o_film.pk)
    except Exception, e:
        return []

    result_list = content_model.Comments.objects.filter(content=content.film_id)[:5]
    try:
        result_list = vbComment(result_list, many=True).data
    except:
        result_list = []

    return result_list


def film_view(request, film_id, *args, **kwargs):
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
    resp_dict['similar'] = calc_similar(o_film)
    resp_dict['comments'] = calc_comments(o_film)

    return HttpResponse(render_page('film', {'film': resp_dict}))
