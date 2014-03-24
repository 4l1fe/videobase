from django.shortcuts import render
from django.http import HttpResponse
from apps.films.models import Persons,Films
import re
import os
from PIL import Image, ImageEnhance
from cStringIO import StringIO
from django.core.files import File
from apps.films.constants import APP_PERSON_PHOTO_DIR
# Create your views here.

def image_refresh(func):

    def wrapper(request):

        url = request.POST.get('image')
        m = re.match('.+[/]static[/]upload[/](?P<type>[^/]+)[/](?P<id>[0-9]+)',url)

        path = re.match('.+(?P<path>[/]static[/].+)',url)
        d = m.groupdict()

        p = Persons.objects.get(pk = int(d['id']))
        im = Image.open('.'+path.groupdict()['path'])

        imc = func(d,im,request)

        imfile = StringIO()

        imc.save(imfile,"PNG")
        imfile.seek(0)

        p.photo.save(os.path.basename(path.groupdict()['path'])+'_resize.png', File(imfile))


        return HttpResponse("OK")

    return wrapper

@image_refresh
def resize_image(d,im,request):



    x = int(request.POST.get('x'))
    y = int(request.POST.get('y'))
    x2 = int(request.POST.get('x2'))
    y2 = int(request.POST.get('y2'))



    imc = im.crop((x, y, x2, y2))

    return imc

@image_refresh
def bri_con(d,im,request):


    br = request.POST.get('br')
    co = request.POST.get('co')
    bre= ImageEnhance.Brightness(im)

    imc =im
    if br:
        imc =bre.enhance(br/100.0)

    con = ImageEnhance.Contrast(imc)
    if co:
        imc =con.enhance(co/100.0)

    return imc
    
