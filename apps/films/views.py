from django.shortcuts import render
from django.http import HttpResponse
from apps.films.models import Persons,Films, FilmExtras
import re
import os
from PIL import Image, ImageEnhance
from cStringIO import StringIO
from django.core.files import File
from apps.films.constants import APP_PERSON_PHOTO_DIR
# Create your views here.
import warnings

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



