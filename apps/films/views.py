from django.http import Http404
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.core.files import File
from django.template import Template, Context
from django.core.context_processors import csrf


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from apps.films.models import Persons, Films, FilmExtras, PersonsFilms, UsersPersons, PersonsExtras, UsersFilms
from apps.contents.models import Comments, Contents

# Do not remove there is something going on when importing, probably models registering itselves
import apps.films.models


from cStringIO import StringIO
from PIL import Image, ImageEnhance
import re
import os
import warnings

# Create your views here.

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

        path = re.match('.+(?P<path>[/]static[/].+)',url)
        d = m.groupdict()

        
        if d['type'] == 'persons':
            p = Persons.objects.get(pk = int(d['id']))
        elif d['type'] == 'filmextras':
            p = FilmExtras.objects.get(pk = int(d['id']))
        else:
            warnings.warn("Unknown type {} of requests for image manipulation")

        im = Image.open('.'+path.groupdict()['path'])

        imc = func(d,im,request)

        imfile = StringIO()

        imc.save(imfile,"PNG")
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
def bri_con(d,im,request):


    br = request.POST.get('br')
    co = request.POST.get('co')
    bre= ImageEnhance.Brightness(im)

    imc =im
    if br:
        imc =bre.enhance(2*(int(br))/100.0)

    coe = ImageEnhance.Contrast(imc)
    if co:
        imc =coe.enhance(2*(int(co))/100.0)

    return imc


class PersonAPIView(APIView):

    def get(self, request, format = None,resource_id = None, extend = False ):
        # Process any get params that you may need
        # If you don't need to process get params,
        # you can skip this part
        #extend = request.GET.get('extend', False)
        #p = Persons.objects.get(pk = kw['resource_id'])
        try:
            p = Persons.objects.get(pk = resource_id)
        except:
            raise Http404
            # Any URL parameters get passed in **kw
        
        response = Response(p.as_vBPerson(extend=='true'), status=status.HTTP_200_OK)
        return response
        

class PersonFilmographyAPIView(APIView):

    def get(self, request, format = None,resource_id = None, extend = False ):

        try:
            p = Persons.objects.get(pk = resource_id)

            pfs = PersonsFilms.objects.filter(person = p)

            vbFilms = [pf.film.as_vbFilm() for pf in pfs]

            
        except Exception,e:
            print e
            raise Http404
            # Any URL parameters get passed in **kw
        
        response = Response(vbFilms, status=status.HTTP_200_OK)
        return response


class PersonActionAPIView(APIView):
    '''

    /api/persons/../action/subscribe

    '''
    def __users_person_set(self,user,person,subscribed):

        try:
            up = UsersPersons.objects.get(user = user,
                                          person = person)
            up.subscribed = subscribed
        except UsersPersons.DoesNotExist, ue:
            up = UsersPersons(user = user,
                              person = person,
                              subscribed=subscribed,
                              upstatus=0 )
        finally:
            up.save()
        
    def _response_template(self,subscribed, request, format = None, resource_id = None):
        '''
        Template for responses
        '''
        
        try:
            person = Persons.objects.get(id=resource_id)
            self.__users_person_set(request.user, person, subscribed)
            response = Response(None, status=status.HTTP_200_OK)
            return response

        except Exception,e:
            print e
            raise Http404
            # Any URL parameters get passed in **kw

            
    def post(self, request, format = None, resource_id = None):
        return self._response_template(1, request, format, resource_id)

    def delete(self, request, format = None, resource_id = None):
        return self._response_template(0, request, format, resource_id)







class PersonsExtrasAPIView(APIView):

    def get(self, request, format=None, resource_id=None, extend=False, type = None):

        try:
            person = Persons.objects.get(id=resource_id)
            if type is None:
                pes = PersonsExtras.objects.filter(person = person)
            else:
                pes = PersonsExtras.objects.filter(person = person, type = type)

            result = [pe.as_vbExtra() for pe in pes]
            
            response = Response(result, status=status.HTTP_200_OK)
            return response

        except Exception,e:
            print e
            raise Http404
            # Any URL parameters get passed in **kw
        


def index_view(request):
        # ... view code here

    return render_to_response('index.html',)

def person_view(request, film_id):
        # ... view code here

    return render_to_response('person.html')

def register_view(request):
        # ... view code here

    return render_to_response('register.html',)

def login_view(request):
        # ... view code here

    return render_to_response('login.html',)


def test_view(request):
    c = Context({})
    c.update(csrf(request))

    # ... view code here
    return render_to_response('api_test.html',c)


