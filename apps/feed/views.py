from django.shortcuts import render
from datetime import datetime
from apps.films.models import Films



def get_feed_tw(request):
    films = Films.get_newest_films().all()
    result = {'films': films, 'date': datetime.utcnow(), 'newdate': ''}
    return render(request, 'tw_feed.html',
                  result)


def get_feed_vk(request):
    films = Films.get_newest_films().all()
    result = {'films': films, 'newdate': '', 'img': ''}
    return render(request, 'vk_feed.html',
                  result)


def get_feed(request):
    films = Films.get_newest_films().all()
    result = {'films': films, 'newdate': ''}
    return render(request, 'feed.html',
                  result)


def get_feed_fb(request):
    films = Films.get_newest_films().all()
    result = {'films': films, 'newdate': ''}
    return render(request, 'fb_feed.html',
                  result)