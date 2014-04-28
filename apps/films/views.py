# coding: utf-8

import re
import os
import warnings

from cStringIO import StringIO
from PIL import Image, ImageEnhance

from django.core.files import File
from django.contrib.auth.models import User
from django.template import Template, Context
from django.http import HttpResponse, Http404
from django.core.context_processors import csrf
from django.shortcuts import render_to_response

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import apps.films.models as film_model
import apps.contents.models as content_model

from apps.users.api.users import vbUser
from apps.films.api.serializers import vbFilm, vbComment

from utils.noderender import render_page

# # Do not remove there is something going on when importing, probably models registering itselves
# import apps.films.models


def get_new_namestring(namestring):

    m = re.match("(?P<pre>.+)v(?P<version>[0-9]+)[.]png",namestring)

    if m is None:
        return namestring + '_v1.png'
    else:
        d = m.groupdict()
        return  '{:s}v{:d}.{:s}'.format(d['pre'],int(d['version']) +1,'png')

      
def image_refresh(func):
    def wrapper(request):
        url = request.POST.get('image')
        m = re.match('.+[/]static[/]upload[/](?P<type>[^/]+)[/](?P<id>[0-9]+)',url)

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
def resize_image(d,im,request):
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
    """

    """

    def get(self, request, format=None, resource_id=None, extend=False):
        # Process any get params that you may need
        # If you don't need to process get params,
        # you can skip this part
        #extend = request.GET.get('extend', False)
        #p = Persons.objects.get(pk = kw['resource_id'])
        try:
            p = film_model.Persons.objects.get(pk = resource_id)
        except:
            raise Http404
            # Any URL parameters get passed in **kw
        
        response = Response(p.as_vBPerson(extend=='true'), status=status.HTTP_200_OK)
        return response
        

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
        
    def _response_template(self,subscribed, request, format=None, resource_id=None):
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


def index_view(request):
    # ... view code here

    return render_to_response('index.html',)


def person_view(request, resource_id):
        # ... view code here
        '''
        - header_title = person.name

        - person_roles = person.roles && person.roles.length?person.roles.join(", "):false
        - person_birthplace = person.birthplace && person.birthplace.length?person.birthplace.join(", "):false
        - person_birthdate = new Date(person.birthdate)
        - person_years_old = how_long(person_birthdate, 0)
        - person_birthdate_string = date_text(person_birthdate) + " г. (" + person_years_old + ")"
        '''

        person = film_model.Persons.objects.get(pk =resource_id)

        pfs = film_model.PersonsFilms.objects.filter(person = person)

        vbFilms = [pf.film.as_vbFilm() for pf in pfs]

        for vbf in vbFilms:
            
            vbf.update({'instock':True,
                        'hasFree':True,
                        'year':vbf['release_date'].strftime('%Y'),
                        'release_date':''
                    })

            
        return HttpResponse(render_page('person',{
            'person' : {'id': resource_id,
                      'name': person.name,
                      'photo': "static/img/tmp/person1.jpg",
                      'bio': person.bio,
                      'birthdate': "1974-01-22",
                      'roles': ["актер", "режиссёр"],
                      'birthplace': ["Москва", "Россия"]},

            'filmography': vbFilms}))


def login_view(request):
    # ... view code here
    pass


def register_view(request):
    # ... view code here
    return HttpResponse(render_page('register',{}))


def user_view(request, resource_id):

    try:
        user = User.objects.get(pk=resource_id)

        uvb = vbUser(user)

        default_user = {'id': -1,
               'friends': [],
               'genres': [],
               'regdate':'2014-01-01',
               }

        default_user.update(uvb.data)

        default={'user':default_user,
                 'films_subscribed': [],
                 'actors_fav': [],
                 'feed': [],
                 'directors_fav':[],
                 'user_how_long':[]
                 }

        return HttpResponse(render_page('user', default))

    except User.DoesNotExist:
        raise Http404


def test_view(request):
    c = Context({})
    c.update(csrf(request))

    return render_to_response('api_test.html', c)

def calc_actors(o_film):
    result_list = []
    try:
        result_list = film_model.Persons.objects.filter(person_film_rel__film=o_film.pk).values('id', 'name')[:5]
    except Exception, e:
        pass

    return result_list

def calc_similar(o_film):
    result_list = []

    try:
        result = film_model.Films.similar_api(o_film)
        for item in result:
            result_list.append({'id': item.id, 'name': item.name, 'rating': item.rating_cons, 'year': item.release_date.strftime("%Y")})
    except Exception, e:
        pass

    return result_list

def calc_comments(o_film):
    try:
        content = content_model.Contents.objects.get(film=o_film.pk)
    except Exception, e:
        return []

    result_list = content_model.Comments.objects.filter(content=content.film_id)[:5]
    return result_list

def transform_to_json_serializable(rdict):
    rdict['releasedate'] = rdict['releasedate'].strftime("%d-%m-%Y")
    rdict['actors'] = [dict(actor) for actor in rdict['actors']]
    return rdict

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

    film = transform_to_json_serializable(resp_dict)
    return HttpResponse(render_page('film', {'film':film}))
