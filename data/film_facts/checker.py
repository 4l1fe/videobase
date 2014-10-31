# coding: utf-8
from datetime import datetime

import gdata.youtube
import gdata.youtube.service

from apps.films.models import Films, FilmExtras, YoutubeTrailerCheck
from apps.films.models import PersonsFilms
from apps.films.models import Countries
from data.checker import FactChecker
from data.constants import FLATLAND_NAME
from crawler.tasks.datarobots_tasks import kinopoisk_parse_one_film
from bs4 import BeautifulSoup
import requests
import re
from apps.films.constants import *
from data.film_facts.trailer_title_check import is_correct_trailer_title


film_checker = FactChecker(Films)


def find_first_pattern_position(str, pat):
        pattern = re.compile(pat)
        mo = re.search(pattern, str)
        if mo:
            return mo.start()
        else:
            return -1


def film_poster_corrector(film):
    try:
        film_extras = FilmExtras.objects.filter(film=film)
        for oneExtra in film_extras:
            if not is_size_of_photo_ok(oneExtra):
                oneExtra.delete()
        film.save()
        print u"Corrector removed film poster"
    except Exception:
        print u"Can't delete film poster"


def youtube_trailer_corrector(film):
    extras = FilmExtras.objects.filter(film=film)
    for film_extra in extras:
        try:
            if not is_trailer_contains_film_name(film, film_extra) or not is_trailer_exists(film_extra)\
                    or not is_trailer_match_key_words(film, film_extra) or not is_trailer_duration_ok(film_extra):
                film_extra.delete()
                YoutubeTrailerCheck.objects.get(film=film).delete()
            print u"Corrector deleted bad trailer successfully"
        except:
            print u"Can't delete trailer"


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


def film_scriptwriter_and_director_corrector(film):
    if film.kinopoisk_id:
        kinopoisk_parse_one_film.apply_async(
                     (
                     film.kinopoisk_id,
                     film.name
                     )
                )
        print u"Corrector updated scriptwriter and director info for film successfully"


def film_no_name_corrector(film):
    if film.kinopoisk_id:
        kinopoisk_parse_one_film.apply_async(
                     (
                     film.kinopoisk_id,
                     film.name
                     )
                )
        print u"Corrector updated film name successfully"


def film_produced_country_name_corrector(film):
    film_countries = film.countries
    dictinary = {}
    a = re.compile("^[a-zA-Z]")
    try:
        with open(os.path.dirname(__file__) + "/../countries") as f:
            for line in f:
                spl_str = line.split('\t')
                if len(spl_str) > 1:
                    key = unicode(spl_str[0], "utf-8").encode("utf-8")
                    val = unicode(spl_str[1], "utf-8").encode("utf-8")
                    dictinary[str(key)] = val

        for fc in film_countries.iterator():
            if a.match(fc.name.encode("utf-8")):
                fc.name = dictinary[fc.name]
                fc.save()
    except:
        print u"Corrector can't translated produced country name to russian"

    print u"Corrector translated produced country name to russian successfully"


def is_flatland_in_countries(film):
    for country in film.countries.all():
        if country.name == FLATLAND_NAME:
            return True
    return False


@film_checker.add(u'Flatland in countries')
def flatland_check(film):
    if not is_flatland_in_countries(film):
        return False
    return True


def is_trailer_contains_film_name(film, film_extra):
    yt_service = gdata.youtube.service.YouTubeService()
    try:
        yid = re.match('.+watch[?]v[=](?P<id>.+)(([&].+)?)', film_extra.url).groupdict()['id']
        entry = yt_service.GetYouTubeVideoEntry(video_id=yid)

        name_orig_cond = film.name_orig.strip() and (film.name_orig.lower() in entry.title.text.decode('utf-8').lower())
        name_cond = film.name.strip() and (film.name.lower() in entry.title.text.decode('utf-8').lower())

        if not(name_cond or name_orig_cond):
            return False
    except Exception, e:
        pass
        #print "#is_trailer_contains_film_name# exception: ", e.message
    return True


@film_checker.add(u"Youtube name doesn't contain film name", corrector=youtube_trailer_corrector)
def youtube_name_check(film):
    extras = FilmExtras.objects.filter(film=film)
    for film_extra in extras:
        if not is_trailer_contains_film_name(film, film_extra):
            return False
    return True


def is_omdb_year_differs_more_than_year(film):
    omdb_id = film.imdb_id
    film_release_date_in_db = film.release_date.year
    try:
        r = requests.get('http://www.omdbapi.com/?i=tt'+str(omdb_id))
        omdb_year_str = r.json()['Released'].split(' ')[2]
        omdb_release_year_date = int(omdb_year_str)
    except :
        print u"Attempt to get film info by imdb id from OMDB server was failed "
        return False

    if omdb_release_year_date and abs(film_release_date_in_db - omdb_release_year_date) > 1:
        return True
    else:
        return False


@film_checker.add(u"Release date differs from OMDB one by more than a year")
def omdb_year_check(film):
    if is_omdb_year_differs_more_than_year(film):
        return False
    return True


def is_trailer_exists(film_extra):
    yt_service = gdata.youtube.service.YouTubeService()
    try:
        yid = re.match('.+watch[?]v[=](?P<id>.+)(([&].+)?)', film_extra.url).groupdict()['id']
        yt_service.GetYouTubeVideoEntry(video_id=yid)
    except Exception, e:
        #print "#is_trailer_exists# exception: ", e.message
        return False
    return True


@film_checker.add(u"There is no such trailer", corrector=youtube_trailer_corrector)
def trailer_exists_check(film):
    extras = FilmExtras.objects.filter(film=film)
    for film_extra in extras:
        if not is_trailer_exists(film_extra):
            return False
    return True


def is_trailer_duration_ok(film_extra):
    max_trailer_time_in_seconds = 270
    min_trailer_time_in_seconds = 60
    yt_service = gdata.youtube.service.YouTubeService()
    try:
        yid = re.match('.+watch[?]v[=](?P<id>.+)(([&].+)?)', film_extra.url).groupdict()['id']
        entry = yt_service.GetYouTubeVideoEntry(video_id=yid)
        trailer_duration = entry.media.duration.seconds
    except Exception, e:
        #print "#is_trailer_duration_ok# exception: ", e.message
        return True
    if trailer_duration:
        trailer_duration = int(trailer_duration)
        if not((trailer_duration >= min_trailer_time_in_seconds) and (trailer_duration <= max_trailer_time_in_seconds)):
            return False
    else:
        return False
    return True


@film_checker.add(u"Youtube trailer duration not within limits", corrector=youtube_trailer_corrector)
def trailer_duration_check(film):
    extras = FilmExtras.objects.filter(film=film)
    for film_extra in extras:
        if not is_trailer_duration_ok(film_extra):
            return False
    return True


def is_trailer_release_date_is_2014(film):
    date_string = '2014'
    date = datetime.strptime(date_string, '%Y')
    return film.release_date.year == date.year


@film_checker.add(u"Film release year is not 2014")
def film_release_date_check(film):
    if not is_trailer_release_date_is_2014(film):
        return False
    return True


def is_kinopoisk_id_set(film):
    film_kinopoisk_id = film.kinopoisk_id
    return film_kinopoisk_id > 0


@film_checker.add(u"Film kinopoisk id is not set")
def film_kinopoisk_id_check(film):
    if not is_kinopoisk_id_set(film):
        return False
    return True


def is_film_no_name(film):
    film_name = film.name
    return film_name == "NoName"


@film_checker.add(u"Film Name is no name", corrector=film_no_name_corrector)
def film_no_name_check(film):
    if is_film_no_name(film):
        return False
    return True


def is_film_description_contains_html(film):
    bs = BeautifulSoup(film.description)
    p_tag = bs.find('body').find('p')
    if p_tag:
        tags_count = len(p_tag.findChildren())
        if tags_count == 0:
            return False
    return True


@film_checker.add(u"Film description contains html tags", corrector=film_description_html_corrector)
def film_description_contains_html_tags_check(film):
    if is_film_description_contains_html(film):
        return False
    return True


def is_film_description_contains_digits(film):
    film_description = film.description
    _digits = re.compile('\d')
    return bool(_digits.search(film_description))


@film_checker.add(u"Film description contains digits", corrector=film_description_digits_corrector)
def film_description_contains_digits_check(film):
    if is_film_description_contains_digits(film):
        return False
    return True


def is_film_description_contains_useless_site_names(film):
    film_description = film.description.encode("utf-8")
    i = find_first_pattern_position(film_description, "(NOW.RU)|(ZOOMBY.RU)")
    return i!=-1


@film_checker.add(u"Film description contains useless site names at the end",
                  corrector=film_description_useless_links_corrector)
def film_description_contains_useless_site_names_check(film):
    if is_film_description_contains_useless_site_names(film):
        return False
    return True


def is_kinopoisk_rating_set(film):
    film_kinopoisk_rating = film.rating_kinopoisk
    if film_kinopoisk_rating:
        return True
    else:
        return False


@film_checker.add(u"Film has no Kinopoisk rating")
def film_kinopoisk_rating_check(film):
    if not is_kinopoisk_rating_set(film):
        return False
    return True


def is_script_writer_ok(persons_film):
    if persons_film.p_type == APP_PERSON_SCRIPTWRITER or persons_film.p_type == APP_PERSON_DIRECTOR:
        return True
    else:
        return False


@film_checker.add(u"Film has no scriptwriter or director", corrector=film_scriptwriter_and_director_corrector)
def film_scriptwriter_check(film):
    persons_film = PersonsFilms.objects.filter(film=film)
    for pf in persons_film:
        if not is_script_writer_ok(pf):
            return False
    return True


def is_produced_country_in_english(film):
    film_countries = film.countries
    a = re.compile("^[a-zA-Z]")
    for i in film_countries.all():
        if a.match(i.name.encode("utf-8")):
            return True
    return False


@film_checker.add(u"Film has produced country name in english", corrector=film_produced_country_name_corrector)
def film_produced_country_name_check(film):
    if is_produced_country_in_english(film):
        return False
    return True


def is_trailer_match_key_words(film, film_extra):
    yt_service = gdata.youtube.service.YouTubeService()
    try:
        yid = re.match('.+watch[?]v[=](?P<id>.+)(([&].+)?)', film_extra.url).groupdict()['id']
        entry = yt_service.GetYouTubeVideoEntry(video_id=yid)
        trailer_title = unicode(entry.title.text, "utf-8").lower()
        if not is_correct_trailer_title(trailer_title, film):
            return False
    except Exception, e:
        pass
        #print u"Trailer title check failed, cause ", "#is_trailer_match_key_words# threw exception ", e.message
    return True


@film_checker.add(u"Film trailer title doesn't contain trailer key words", corrector=youtube_trailer_corrector)
def trailer_title_check(film):
    extras = FilmExtras.objects.filter(film=film)
    for film_extra in extras:
        if not is_trailer_match_key_words(film_extra):
            return False
    return True


def is_size_of_photo_ok(film_extra):
    try:
        if film_extra.photo.size < 2000:
            return False
    except Exception, e:
        pass
       # print "#is_size_of_photo_ok# exception: ", e.message

    return True


@film_checker.add(u"Film has incorrect poster size", corrector=film_poster_corrector)
def film_poster_size_check(film):
    film_extras = FilmExtras.objects.filter(film=film)
    if not film_extras:
        return True
    for oneExtra in film_extras:
        if not is_size_of_photo_ok(oneExtra):
            return False
    return True
