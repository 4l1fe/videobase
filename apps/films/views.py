from django.http import Http404
from django.shortcuts import render
from django.http import HttpResponse
from apps.films.models import Persons,Films, FilmExtras, PersonsFilms, UsersPersons
from apps.users.models import Users
import re
import os
from PIL import Image, ImageEnhance
from cStringIO import StringIO
from django.core.files import File
from apps.films.constants import APP_PERSON_PHOTO_DIR
from django.template import Template, Context

from django.core.context_processors import csrf
from django.shortcuts import render_to_response


# Create your views here.
import warnings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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


    def __users_person_set(self,user,person_id,subscribed):

            
            p = Persons.objects.get(id = person_id)

            try:
                up = UsersPersons.objects.get(user = user,
                                         person = p)
                up.subscribed = subscribed
            except:
                up = UsersPersons(user = user,
                                  person = p,
                                  subscribed=subscribed,
                                  upstatus=0 )
        
    
    def get(self, request, format = None, resource_id = None):

        #try:
        if True:
            
            self.__users_person_set(request.user,resource_id,1)
            response = Response({'status':unicode(request.user)}, status=status.HTTP_200_OK)

            return response
        try:
            pass
        except Exception,e:
            print e
            raise Http404
            # Any URL parameters get passed in **kw

    def delete(self, request, format = None, resource_id = None):

        try:

            print 1
            print resource_id
            print 2
            
            self.__users_person_set(request.user,resource_id,0)
            response = Response({'status':unicode(request.user)}, status=status.HTTP_200_OK)

            return response
        except Exception,e:
            print e
            raise Http404
            # Any URL parameters get passed in **kw


    
def test_view(request):


    template = Template("""

                        <html>
                        <head>
                        <script src="//ajax.googleapis.com/ajax/libs/jquery/2.1.0/jquery.min.js"></script>
                        </head>
                        <body>
                        <script>
// Helper function for csrf
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
                        function csrfSafeMethod(method) {
                            // these HTTP methods do not require CSRF protection
                            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
                        }
                        csrftoken =getCookie("csrftoken")
                        $.ajaxSetup({
                            crossDomain: false, // obviates need for sameOrigin test
                            beforeSend: function(xhr, settings) {
                                if (!csrfSafeMethod(settings.type)) {
                                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                                }
                             }
                        });
                        </script>
                        {%csrf_token%}
                        </body>
                        </html>

                        """)


    c = Context({})
    c.update(csrf(request))
    
    # ... view code here
    return HttpResponse(template.render(c))

    