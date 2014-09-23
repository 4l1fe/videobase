# coding: utf-8

import os
import re
import csv
import codecs
import datetime
import HTMLParser

from django.db import transaction
from django.core.management.base import BaseCommand, CommandError

from apps.films.constants import *
from apps.films.models import Films, Genres, Countries, PersonsFilms, FilmExtras, Persons


class Command(BaseCommand):
    def __init__(self):
        super(Command, self).__init__()
        self.charset = ''

    def handle(self, *args, **options):
        filename = args[0]
        if os.path.exists(filename):
            self.stdout.write(u'Start: Import from UNH CSV from {0}'.format(filename))
            self.import_file(filename)
        else:
            raise Exception(u'File {0} not found'.format(filename))

    @property
    def html_parser(self):
        if not hasattr(self, 'h'):
            self.h = HTMLParser.HTMLParser()

        return self.h

    def escape_html(self, value):
        _value = self.html_parser.unescape(value).strip()
        return _value

    def import_file(self, filename):
        self.stdout.write(u'Run import - {0}'.format(filename))
        data = self.__csvfile(filename)
        headers = data[0]
        counter = 0
        rows = []
        for row in data[1:]:
            rows.append(row)
            if ((counter % 100) == 0):
                self.chunk_insert(rows, headers)
                rows = []

            counter += 1
            if ((counter % 100) == 0):
                self.stdout.write(u'Inserted  {0} items'.format(counter))

        self.stdout.write(u'Inserted  {0} items'.format(counter))

    @transaction.commit_on_success
    def chunk_insert(self, rows, headers):
        for row in rows:
            item = dict(zip(headers, row)) if (len(headers) <= len(row)) else dict(map(None, headers, row))
            self.insert_item(item)
        return True


    def charset_csv_reader(self, csv_data, dialect=csv.excel,
                           charset='utf-8', **kwargs):
        csv_reader = csv.reader(self.charset_encoder(csv_data, charset),
                                dialect=dialect, delimiter='|',
                                lineterminator="\r\n", **kwargs)
        for row in csv_reader:
            yield [unicode(cell, charset) for cell in row]

    def charset_encoder(self, csv_data, charset='utf-8'):
        for line in csv_data:
            yield line.encode(charset)

    def __csvfile(self, datafile):
        self.charset='utf-8'
        csvfile = codecs.open(datafile, 'r', self.charset)
        return list(self.charset_csv_reader(csv_data=csvfile,
                                            charset=self.charset))

    def insert_item(self, data):
        try:
            film = self.get_film(data)
            film.genres = self.get_genres(genres=data['genre_ru'])
            film.countries = self.get_countries(countries=u'Флатландию')
            film.save()
            self.save_trailer(film, data)
            self.save_actors(film, data)
            self.save_director(film, data)

            return True
        except Exception, ex:
            print u'====data==== #{0}=='.format(data["id"])
            print u'====ex====== {0} =='.format(data)
            print ex.message
            print ex.__class__.__name__

            #print('====data==== #{0}=='.format(data.__repr__()))
            return False

    def get_film(self, data):
        attributes = {
            'name': self.escape_html(self.film_name(data)),
            'name_orig': self.escape_html(self.film_name_orig(data)),
            'description': self.escape_html(self.film_description(data)),
            'ftype': APP_FILM_FULL_FILM,
            'kinopoisk_id': data['id_kinopoisk'],
            'frelease_date': self.date_or_now(data['release']),
            'rating_imdb': self.to_float(data['vote_imdb']),
            'rating_imdb_cnt': self.to_int(data['vote_imdb_number']),
            'fduration': self.null_to_none(data['length']),
            'imdb_id': self.null_to_none(data['id_imdb'])
        }
        try:
            film = Films.objects.get(name=attributes['name'])
        except Exception, ex:
            film = Films(**attributes)
            film.save()

        return film

    def to_float(self, value):
        try:
            return float(value)
        except:
            return 0

    def to_int(self, value):
        try:
            return int(value)
        except:
            return 0

    def null_to_none(self, value=None):
        if value is None:
            return None

        if value.lower() == 'null' or value.lower() == '\\n':
            return None

        return value

    def film_description(self, data):
        list_desc = [data['description_ru'], data['description_eng']]
        lists = filter(lambda v: ((not v is None) and (v.lower() != '\\n')), list_desc)
        return lists[0] if lists else ''

    def film_name(self, data):
        list_names = [data['title_ru'], data['title_eng'], data['title_orig']]
        lists = filter(lambda v: ((not v is None) and (v.lower() != '\\n')), list_names)
        return lists[0] if lists else ''

    def film_name_orig(self, data):
        list_names = [data['title_orig'], data['title_eng']]
        lists = filter(lambda v: ((not v is None) and (v.lower() != '\\n')), list_names)
        return lists[0] if lists else ''

    def save_trailer(self, film, data=None):
        if data is None:
            return True

        trailer_youtube_id = data['trailer_youtube']
        if (trailer_youtube_id is None) or (trailer_youtube_id.lower() == '\\n'):
            return True

        youtube_url = "https://www.youtube.com/watch?v=" + trailer_youtube_id
        try:
            traler = FilmExtras.get(url=youtube_url,
                                    etype=APP_FILM_TYPE_ADDITIONAL_MATERIAL_TRAILER)
        except:
            traler = FilmExtras(film=film, name=film.name, name_orig=film.name_orig,
                                url=youtube_url, etype=APP_FILM_TYPE_ADDITIONAL_MATERIAL_TRAILER)
            traler.save()
        return True

    def get_person(self, person_name):
        try:
            person_model = Persons.objects.get(name=self.escape_html(person_name))
        except:
            person_model = Persons(name=self.escape_html(person_name),
                                   name_orig=self.escape_html(person_name))
            person_model.save()
        return person_model

    def save_person_film(self, film, person, p_type):
        try:
            person_film = PersonsFilms.objects.get_or_create(film=film, person=person, p_type=p_type)
            return person_film
        except Exception, e:
            return True

    def save_actors(self, film, data=None):
        actors_names = self.compact_list(self.escape_html(data['actors_eng']).split(','))
        for actor_name in actors_names:
            actor = self.get_person(actor_name)
            self.save_person_film(film, actor, APP_PERSON_ACTOR)
        return True

    def save_director(self, film, data=None):
        directors_names = self.compact_list(data['director_eng'].split(','))
        for director_name in directors_names:
            director = self.get_person(director_name)
            self.save_person_film(film, director, APP_PERSON_DIRECTOR)

        return True

    def compact_list(self, list=None):
        if list is None:
            list = []

        return [el for el in list if (not el is None) and (el.lower() != '\\n')]

    def date_or_now(self, date=None):
        if date is None:
            return datetime.datetime.now()
        if self.is_null(date):
            return datetime.datetime.now()
        try:
            return datetime.datetime.strptime(date, '%Y-%m-%d')
        except:
            return datetime.datetime.now()

    def is_null(self, value=None):
        if value is None:
            return True
        return value.lower() == 'null' or value.lower() == '\\n'

    def get_genres(self, genres=None):
        if genres is None:
            return []

        if not(hasattr(self, 'genres')):
            self.genres = {}
            print(u'====ex====== load genres ==')
            for item in Genres.objects.all():
                self.genres[item.name] = item

        genre_names = map(lambda v: v.strip(), genres.split(','))
        genre_models = []
        for genre_name in genre_names:
            try:
                genre_model = self.genres[genre_name]
            except Exception, e:
                genre_model = Genres(name=genre_name)
                genre_model.save()
                self.genres[genre_name] = genre_model

            genre_models.append(genre_model)

        return genre_models

    def get_countries(self, countries=None):
        if countries is None:
            return []

        if not(hasattr(self, 'countries')):
            print(u'====ex====== load countries ==')
            self.countries = {}
            for item in Countries.objects.all():
                self.countries[item.name] = item

        country_names = map(lambda v: v.strip(), countries.split(','))
        country_models = []
        for country_name in country_names:
            try:
                country_model = self.countries[country_name]
            except Exception, e:
                country_model = Countries(name=country_name)
                country_model.save()
                self.countries[country_name] = country_model

            country_models.append(country_model)

        return country_models

#SELECT * INTO OUTFILE '/tmp/name.csv'
#FIELDS TERMINATED BY '#'
#OPTIONALLY ENCLOSED BY '\"'
#ESCAPED BY '\\'
#LINES TERMINATED BY '\n'
#FROM movies;
