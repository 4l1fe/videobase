# coding: utf-8

import re
from bs4 import BeautifulSoup

from django.utils.timezone import now, datetime

from apps.films.constants import APP_FILM_FULL_FILM
from apps.films.models import Films, PersonsFilms, Persons, Genres, Countries

from crawler.tor import simple_tor_get_page as simple_get
from crawler.datarobots.kinopoisk_ru.parse_page import acquire_page, extract_facts_from_dump

from utils.common import traceback_own


LIMIT = 10
KINOPOISK = 'www.kinopoisk.ru'
dirty_words = (u'(ТВ)', u'(видео)')


def get_link_from_html(html):
    soup = BeautifulSoup(html)
    return soup.find('div', {'class': ['most_wanted']}).\
        find('div', {'class': 'info'}).find('a')['href']


def get_id_by_film(film, load_function=simple_get):
    params = {
        'first': 'no',
        'what': '',
        'kp_query': film.name
    }

    url = 'http://{url}/{page}'.format(url=KINOPOISK, page='index.php')
    response = load_function(url, params=params)

    href = get_link_from_html(response.text)
    return int(re.findall(r'/film/(\d+)', href)[0])


def get_person(name, kinopoisk_id):
    try:
        person = Persons.objects.get(kinopoisk_id=kinopoisk_id)
    except Persons.DoesNotExist:
        person = Persons(name=name, photo='', kinopoisk_id=kinopoisk_id)
        person.save()

        print u"Added Person {person_name}".format(person_name=name)

    return person


def get_genre(name):
    name = name.lower().strip()
    try:
        genre = Genres.get_all_genres(get_values=False).get(name=name)
    except Genres.DoesNotExist:
        genre = Genres.add_root(name=name, description='')
        genre.save()

        print u"Added Genre {genre_name}".format(genre_name=name)

    return genre


def get_country(name):
    try:
        country = Countries.objects.get(name=name)
    except Countries.DoesNotExist:
        country = Countries(name=name, description='')
        country.save()

        print u"Added Country {country_name}".format(country_name=name)

    return country


def process_person_dict(film, person_dict):
    try:
        print u"Found person {person}".format(person=person_dict['name'])
        o_person = get_person(person_dict['name'], person_dict['kinopoisk_id'])

        if not PersonsFilms.objects.filter(film=film, person=o_person).count():
            msg = u"Adding link for film {film} and person {person}"
            print msg.format(film=film, person=o_person)

            params = {
                'person': o_person,
                'film': film,
                'p_type': person_dict['p_type']
            }

            person_film = PersonsFilms(**params)
            person_film.save()

    except Exception, e:
        msg = u"Exception caught in process_person_dict"
        traceback_own(e, msg=msg)


def process_genre_dict(film, genre_dict):
    o_genre = get_genre(genre_dict['name'])
    if not o_genre in film.genres.all():
        msg = u"Setting {genre} genre for {film}"
        print msg.format(genre=o_genre, film=film)

        film.genres.add(o_genre)


def process_country_dict(film, country_dict):
    o_country = get_country(country_dict['name'])
    if not o_country in film.countries.all():
        msg = u"Adding {country} country to {film} film"
        print msg.format(country=o_country, film=film)

        film.countries.add(o_country)


def process_film_facts(film, facts):
    '''
    This function accepts pdata object which contains parsed informaition
    and film object for film that this informaition should be updated from that
    pdata object
    '''
    film_array = []

    for data_entry in facts['Films']:
        film_array.extend(data_entry.items())

    for key, value in dict(film_array).items():
        setattr(film, key, value)

    film.kinopoisk_lastupdate = now()
    film.save()

    print u"Updated data for {film}".format(film=film)
    for person_dict in facts['Persons']:
        process_person_dict(film, person_dict)

    for genre_dict in facts['Genres']:
        process_genre_dict(film, genre_dict)

    for country_dict in facts['Countries']:
        process_country_dict(film, country_dict)

    print u"Saving {film} film object".format(film=film)
    film.save()


def parse_from_kinopoisk(kinopoisk_id, name=None, film=None):
    '''
    Parse page of film with kinopoisk_id from kinopoisk.ru site
    '''
    if film is None:
        try:
            film = Films.objects.get(kinopoisk_id=kinopoisk_id)
        except Films.DoesNotExist:
            for word in dirty_words:
                if word in name:
                    name = name.replace(word, '').strip()
            msg = u"Creating new film object with name {name} and kinopoisk_id: {id}"
            print msg.format(name=name, id=kinopoisk_id)

            params = {
                'kinopoisk_id': kinopoisk_id,
                'name': name if name else u' ',
                'type': APP_FILM_FULL_FILM,
                'release_date': datetime.utcfromtimestamp(0),
                'world_release_date': datetime.utcfromtimestamp(0),
            }

            film = Films(**params)
            film.save()

    try:
        page_dump = acquire_page(film.kinopoisk_id)
        facts = extract_facts_from_dump(page_dump)
        process_film_facts(film, facts)
    except Exception, e:
        msg = u"Caught Exception in parse_from_kinopoisk"
        traceback_own(e, msg=msg)
