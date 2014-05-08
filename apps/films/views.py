# coding: utf-8

import re
import os
import warnings

from cStringIO import StringIO
from PIL import Image, ImageEnhance

from django.core.files import File
from django.core.paginator import Paginator
from django.template import Context
from django.http import HttpResponse, Http404
from django.core.context_processors import csrf
from django.shortcuts import render_to_response

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import apps.films.models as film_model
from apps.films.api.serializers import vbFilm, vbComment, vbPerson
from apps.films.api.serializers.vb_film import GenresSerializer
import apps.contents.models as content_model

from utils.noderender import render_page

# Do not remove there is something going on when importing, probably models registering itselves
# import apps.films.models


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


class PersonAPIView(APIView):

    def get(self, request, format=None, resource_id=None):
        try:
            p = film_model.Persons.objects.get(pk=resource_id)
            data = vbPerson(p).data
            u = request.user
            if u and u.is_authenticated():
                data = vbPerson(p, user=u).data
            return Response(data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def post(self, request, format=None, resource_id=None):
        extend = request.DATA.get('extend', '')
        if extend.lower() == 'true':
            extend = True
        else:
            extend = False

        try:
            p = film_model.Persons.objects.get(pk=resource_id)
            data = vbPerson(p, extend=extend).data
            u = request.user
            if u and u.is_authenticated():
                data = vbPerson(p, extend=True, user=u).data
            return Response(data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


class PersonFilmographyAPIView(APIView):
    """

    """

    def get(self, request, format=None, resource_id=None, extend=False):
        try:
            p = film_model.Persons.objects.get(pk=resource_id)
            pfs = film_model.PersonsFilms.objects.filter(person=p)
            vbFilms = [pf.film.as_vbFilm() for pf in pfs]
        except Exception,e:
            raise Http404

        return Response(vbFilms, status=status.HTTP_200_OK)


class PersonActionAPIView(APIView):
    '''

    '''

    def __users_person_set(self, user, person, subscribed):
        filter = {
            'user': user,
            'person': person,
        }

        try:
            up = film_model.UsersPersons.objects.get(**filter)
            up.subscribed = subscribed
        except film_model.UsersPersons.DoesNotExist, ue:
            up = film_model.UsersPersons(subscribed=subscribed, upstatus=0, **filter)
        finally:
            up.save()
        
    def _response_template(self, subscribed, request, format=None, resource_id=None):
        '''
        Template for responses
        '''

        try:
            person = film_model.Persons.objects.get(id=resource_id)
            self.__users_person_set(request.user, person, subscribed)
            return Response(status=status.HTTP_200_OK)
        except Exception, e:
            raise Http404

    def post(self, request, format=None, resource_id=None):
        return self._response_template(1, request, format, resource_id)

    def delete(self, request, format=None, resource_id=None):
        return self._response_template(0, request, format, resource_id)


class PersonsExtrasAPIView(APIView):
    """

    """

    def get(self, request, format=None, resource_id=None, extend=False, type=None):
        try:
            filter = {
                'person': film_model.Persons.objects.get(id=resource_id)
            }
            if not type is None:
                filter.update({'type': type})

            pes = film_model.PersonsExtras.objects.filter(**filter)
            result = [pe.as_vbExtra() for pe in pes]
            return Response(result, status=status.HTTP_200_OK)
        except Exception, e:
            raise Http404


def transform_vbFilms(vbf):

    vbf.update({'instock': True,
        'hasFree': True,
        'year': vbf['releasedate'].strftime('%Y'),
        'releasedate': vbf['releasedate'].strftime('%Y-%m-%d'),
        })

    return vbf


def index_view(request):
    # ... view code here

    o_film = film_model.Films.objects.order_by('-release_date').all()[:4]

    resp_dict = vbFilm(o_film, extend=True, many=True)
    data = resp_dict.data

    o_genres = GenresSerializer(film_model.Genres.objects.all(), many=True)

    print "fds", o_genres.data
    
    genres = [{'id': g['id'],'name': g['name']} for g in o_genres.data]

    
    
    #try:

    resp_data = [transform_vbFilms(vbf) for vbf in data]
    #except:
    #    raise Http404
    
    

    
    return HttpResponse(render_page('index', {'new_films': resp_data, 'genres':o_genres.data}), status.HTTP_200_OK)


def person_view(request, resource_id):

    try:
        person = film_model.Persons.objects.get(pk=resource_id)
    except film_model.Persons.DoesNotExist:
        raise Http404
    vbp = vbPerson(person, extend=True)
    pfs = film_model.PersonsFilms.objects.filter(person=person)
    page = Paginator(pfs, 12).page(1)
    pfs = page.object_list
    vbFilms = vbFilm([pf.film for pf in pfs], many =True)
    return HttpResponse(render_page('person',
                                    {'person': vbp.data,
                                     'filmography': vbFilms.data}))


def test_view(request):
    c = Context({})
    c.update(csrf(request))

    return render_to_response('api_test.html', c)


def calc_actors(o_film):
    result_list = []
    try:
        result_list = list(film_model.Persons.objects.filter(person_film_rel__film=o_film.pk).values('id', 'name')[:5])
    except Exception, e:
        pass

    return result_list


def calc_similar(o_film):
    result_list = []

    try:
        result = film_model.Films.similar_api(o_film)
        for item in result:
             result_list.append({
                 'id': item.id,
                 'name': item.name,
                 'ratings': item.get_rating_for_vb_film,
                 'year': item.release_date.strftime("%Y"),
                 #TODO: надо вычислять
                 'poster': "static/img/tmp/poster1.jpg",
                 'relation': {'rating': 5},
                 'instock': True,
                 'hasFree': True,
             })
    except Exception, e:
        pass

    return result_list


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
    resp_dict = {}
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

