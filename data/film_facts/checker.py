# coding: utf-8
from apps.films.models import Films, FilmExtras

from apps.films.models import Countries

from data.checker import FactChecker
from data.constants import FLATLAND_NAME
import gdata.youtube
import gdata.youtube.service
import re


film_checker = FactChecker(Films)


@film_checker.add(u'Flatland in countries')
def flatland_check(film):
    flatland = Countries.objects.get(name = FLATLAND_NAME)
    return not ( flatland in film.countries.all() )


@film_checker.add(u"Youtube name doesn't contain film name")
def youtube_name_check(film):

    yt_service = gdata.youtube.service.YouTubeService()
    ft = FilmExtras.objects.filter(film = film)[0]
    yid = re.match('.+watch[?]v[=](?P<id>.+)(([&].+)?)', ft.url).groupdict()['id']

    entry =yt_service.GetYouTubeVideoEntry(video_id=yid)

    #print film.name, entry.title.text
    #print 'name = "{}"'.format(film.name_orig)

    #print film.name.lower() in entry.title.text.decode('utf-8').lower()
    #print (film.name_orig.lower() in entry.title.text.decode('utf-8').lower()) and film.name_orig.strip() ==''

    name_orig_cond = film.name_orig.strip() and (film.name_orig.lower() in entry.title.text.decode('utf-8').lower())
    name_cond = film.name.strip() and (film.name.lower() in entry.title.text.decode('utf-8').lower()) 

    return name_cond or name_orig_cond
    


@film_checker.add(u"Release date differs from omdb one by more than a year")
def omdb_year_check(film):
    pass


@film_checker.add("There is no such trailer")
def trailer_check(film):
    pass

@film_checker.add("Youtube trailer duration not within limits")
def trailer_duration_check(film):
    pass



    
    





