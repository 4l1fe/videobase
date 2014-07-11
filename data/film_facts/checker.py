# coding: utf-8
from datetime import datetime
import re

import gdata.youtube
import gdata.youtube.service

from apps.films.models import Films, FilmExtras
from apps.films.models import Countries
from data.checker import FactChecker
from data.constants import FLATLAND_NAME
from bs4 import BeautifulSoup
import requests
import re


film_checker = FactChecker(Films)


def find_first_pattern_position(str, pat):
        pattern = re.compile(pat)
        mo = re.search(pattern, str)
        if mo:
            return mo.start()
        else:
            return -1


def youtube_trailer_corrector(film):
    ft = FilmExtras.objects.filter(film=film).first()
    ft.delete()
    print u"Corrector deleted bad trailer successfully"


def film_description_html_corrector(film):
    film_html_description = BeautifulSoup(film.description)
    film.description = film_html_description.getText(separator=u' ')
    film.save()
    print u"Corrector removed html tags in film description"


def film_description_digits_corrector(film):
    film_description = film.description.encode("utf-8")

    i = find_first_pattern_position(film_description, "[А-Я]")
    if i!=-1:
        film.description = film_description[i:].decode("utf-8")
        film.save()
        print u"Corrector removed digits in film description"


def film_description_useless_links_corrector(film):
    film_description = film.description.encode("utf-8")

    i = find_first_pattern_position(film_description, "(NOW.RU)|(ZOOMBY.RU)")
    if i!=-1:
        film.description = film_description[0:i].decode("utf-8")
        film.save()
        print u"Corrector removed useless links in film description"



@film_checker.add(u'Flatland in countries')
def flatland_check(film):
    flatland = Countries.objects.get(name = FLATLAND_NAME)
    return not ( flatland in film.countries.all() )


@film_checker.add(u"Youtube name doesn't contain film name", corrector=youtube_trailer_corrector)
def youtube_name_check(film):

    yt_service = gdata.youtube.service.YouTubeService()
    try:
        ft = FilmExtras.objects.filter(film = film).first()
        yid = re.match('.+watch[?]v[=](?P<id>.+)(([&].+)?)', ft.url).groupdict()['id']
        entry = yt_service.GetYouTubeVideoEntry(video_id=yid)
    except:
        return True

    #print film.name, entry.title.text
    #print 'name = "{}"'.format(film.name_orig)

    #print film.name.lower() in entry.title.text.decode('utf-8').lower()
    #print (film.name_orig.lower() in entry.title.text.decode('utf-8').lower()) and film.name_orig.strip() ==''

    name_orig_cond = film.name_orig.strip() and (film.name_orig.lower() in entry.title.text.decode('utf-8').lower())
    name_cond = film.name.strip() and (film.name.lower() in entry.title.text.decode('utf-8').lower())

    return name_cond or name_orig_cond



@film_checker.add(u"Release date differs from omdb one by more than a year")
def omdb_year_check(film):
    omdb_id = film.imdb_id
    film_release_date_in_db = film.release_date.year

    try:
        r = requests.get('http://www.omdbapi.com/?i=tt'+str(omdb_id))
        omdb_year_str = r.json()['Released'].split(' ')[2]
        omdb_release_year_date = int(omdb_year_str)
    except :
        print u"Attempt to get film info by imdb id from OMDB server was failed "
        return True

    if omdb_release_year_date and abs(film_release_date_in_db - omdb_release_year_date) > 1:
        return False
    else:
        return True


@film_checker.add(u"There is no such trailer", corrector=youtube_trailer_corrector)
def trailer_check(film):
    yt_service = gdata.youtube.service.YouTubeService()
    ft = FilmExtras.objects.filter(film=film).first()
    try:
        yid = re.match('.+watch[?]v[=](?P<id>.+)(([&].+)?)', ft.url).groupdict()['id']
        entry = yt_service.GetYouTubeVideoEntry(video_id=yid)
        return True
    except:
        return False


@film_checker.add(u"Youtube trailer duration not within limits", corrector=youtube_trailer_corrector)
def trailer_duration_check(film):
    max_trailer_time_in_seconds = 270
    min_trailer_time_in_secons = 60
    yt_service = gdata.youtube.service.YouTubeService()
    try:
        ft = FilmExtras.objects.filter(film=film).first()
        yid = re.match('.+watch[?]v[=](?P<id>.+)(([&].+)?)', ft.url).groupdict()['id']
        entry = yt_service.GetYouTubeVideoEntry(video_id=yid)
        trailer_duration = entry.media.duration.seconds
    except:
        return True
    if trailer_duration:
        trailer_duration = int(trailer_duration)
        if (trailer_duration >= min_trailer_time_in_secons) and (trailer_duration <= max_trailer_time_in_seconds):
            return True
        else:
            return False
    else:
        return False


@film_checker.add(u"Film release year is not 2014")
def film_release_date_check(film):
    date_string = '2014'
    date = datetime.strptime(date_string, '%Y')
    return film.release_date.year == date.year


@film_checker.add(u"Film kinopoisk id is not set")
def film_kinopoisk_id_check(film):
    film_kinopoisk_id = film.kinopoisk_id
    if film_kinopoisk_id > 0:
        return True
    else:
        return False


@film_checker.add(u"Film description contains html tags", corrector=film_description_html_corrector)
def film_description_contains_html_tags_check(film):
    bs = BeautifulSoup(film.description)
    p_tag = bs.find('body').find('p')
    if p_tag:
        tags_count = len(p_tag.findChildren())
        if tags_count == 0:
            return True
    return False


@film_checker.add(u"Film description contains digits", corrector=film_description_digits_corrector)
def film_description_contains_digits_check(film):
    film_description = film.description
    a = re.compile("^[А-Я]")
    if a.match(film_description.encode("utf-8")):
        return True
    else:
        return False


@film_checker.add(u"Film description contains useless site names at the end",
                  corrector=film_description_useless_links_corrector)
def film_description_contains_useless_site_names_check(film):
    film_description = film.description.encode("utf-8")
    i = find_first_pattern_position(film_description, "(NOW.RU)|(ZOOMBY.RU)")
    if i!=-1:
        return False
    else:
        return True


@film_checker.add(u"Film has no Kinopoisk rating")
def film_kinopoisk_rating_check(film):
    film_kinopoisk_rating = film.rating_kinopoisk
    if film_kinopoisk_rating:
        return True
    else:
        return False
