from django.shortcuts import render, get_object_or_404, HttpResponse
from models import About, Legal


def legal(request):
    l = Legal.objects.first()
    if not l:
        return HttpResponse('')
    return HttpResponse(l.text)


def about(request):
    a = About.objects.first()
    if not a:
        return HttpResponse('')
    return HttpResponse(a.text)