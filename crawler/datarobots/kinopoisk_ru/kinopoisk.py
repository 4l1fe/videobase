# coding: utf-8

import re
from bs4 import BeautifulSoup

from django.utils.timezone import now, datetime

from apps.films.constants import APP_FILM_FULL_FILM
from apps.films.models import Films, PersonsFilms, Persons, Genres, Countries

from crawler.tor import simple_tor_get_page as simple_get
from crawler.datarobots.kinopoisk_ru.parse_page import acquire_page, extract_facts_from_dump

LIMIT = 10
KINOPOISK = 'www.kinopoisk.ru'


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

    url = "http://%s/%s" % (KINOPOISK, 'index.php')
    response = load_function(url, params=params)

    href = get_link_from_html(response.text)
    return int(re.findall(r'/film/(\d+)', href)[0])


def get_person(name, kinopoisk_id):
    try:
        person = Persons.objects.get(kinopoisk_id=kinopoisk_id)
    except Persons.DoesNotExist:
        person = Persons(name=name, photo='', kinopoisk_id=kinopoisk_id)
        person.save()
        print u'Added Person {}'.format(name)

    return person


def get_genre(name):
    name = name.lower().strip()
    try:
        genre = Genres.get_all_genres().get(name=name)
    except Genres.DoesNotExist:
        genre = Genres(name=name, description='')
        genre.save()
        print u'Added Genre {}'.format(name)

    return genre


def get_country(name):
    try:
        country = Countries.objects.get(name=name)
    except Countries.DoesNotExist:
        country = Countries(name=name, description='')
        country.save()
        print u'Added Country {}'.format(name)

    return country

flatland = get_country(u'Флатландию')


def process_person_dict(film, person_dict):
    try:
        print u"Found person {}".format(person_dict['name'])
        person_object = get_person(person_dict['name'], person_dict['kinopoisk_id'])

        if not PersonsFilms.objects.filter(film=film, person=person_object).count():
            print u"Adding link for film {} and person {}".format(film, person_object)
            person_film = PersonsFilms(person=person_object, film=film, p_type=person_dict['p_type'])
            person_film.save()
    except Exception, e:
        print e


def process_genre_dict(film, genre_dict):
    genre_object = get_genre(genre_dict['name'])
    if not genre_object in film.genres.all():
        print u"Setting {} genre for {}".format(genre_object, film)
        film.genres.add(genre_object)


def process_country_dict(film, country_dict):
    if flatland in film.countries.all():
        film.countries.remove(flatland)

    country_object = get_country(country_dict['name'])
    if not country_object in film.countries.all():
        print u"Adding {} country to {} film".format(country_object, film)
        film.countries.add(country_object)


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

    print u"Updated data for {}".format(film)
    for person_dict in facts['Persons']:
        process_person_dict(film, person_dict)

    for genre_dict in facts['Genres']:
        process_genre_dict(film, genre_dict)

    for country_dict in facts['Countries']:
        process_country_dict(film, country_dict)

    print u"Saving {} film object".format(film)
    film.save()


def parse_from_kinopoisk(kinopoisk_id, name=None, film=None):
    '''
    Parse page of film with kinopoisk_id from kinopoisk.ru site
    '''
    if film is None:
        try:
            film = Films.objects.get(kinopoisk_id=kinopoisk_id)
        except Films.DoesNotExist:
            print u"Creating new film object with name {} and kinopoisk_id {}".format(name, kinopoisk_id)
            film = Films(kinopoisk_id=kinopoisk_id,
                         name=name if name else u' ',
                         type=APP_FILM_FULL_FILM,
                         release_date=datetime.utcfromtimestamp(0))
            film.save()

    try:
        page_dump = acquire_page(film.kinopoisk_id)
        facts = extract_facts_from_dump(page_dump)
        process_film_facts(film, facts)
    except Exception, exception:
        print exception
