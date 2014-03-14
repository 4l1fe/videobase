# coding: utf-8

import os, csv, re
from datetime import datetime
import codecs
import chardet
import datetime
import warnings

from django.db import DatabaseError
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import LabelCommand, BaseCommand, CommandError
from optparse import make_option
from django.db import models
from django.contrib.contenttypes.models import ContentType

from apps.films.constants import *
from apps.films.models import Films, Genres, Countries

class Command(BaseCommand):
    def __init__(self):
        super(Command, self).__init__()
        self.charset = ''

    def handle(self, *args, **options):
        filename =  args[0]
        if os.path.exists(filename):
            self.stdout.write('Start: Import from UNH CSV from %s' % filename)
            self.import_file( filename)
        else:
            raise Exception('File %s not found' % filename)

    def import_file(self, filename):
        self.stdout.write('Run import -  %s' % filename)
        data = self.__csvfile(filename)
        headers = data[0]
        counter = 0

        for row in data[1:100]:
            item = dict(zip(headers, row)) if (len(headers) <= len(row)) else dict(map(None, headers, row))
            if self.insert_item(item):
                counter += 1
            if ((counter % 100) == 0):
                self.stdout.write('Inserted  {0} items'.format(counter))

        self.stdout.write('Inserted  {0} items'.format(counter))

    def charset_csv_reader(self, csv_data, dialect=csv.excel,
                           charset='utf-8', **kwargs):
        csv_reader = csv.reader(self.charset_encoder(csv_data, charset),
                                dialect=dialect, delimiter=';', **kwargs)
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
            attributes = {
                'name': self.film_name(data),
                'name_orig': self.film_name_orig(data),
                'description': self.film_description(data),
                'ftype': APP_FILM_FULL_FILM,
                'kinopoisk_id': data['id_kinopoisk'],
                'frelease_date': self.date_or_now(data['release']),
                'rating_imdb': data['vote_imdb'],
                'rating_imdb_cnt': data['vote_imdb_number'],
                'fduration': self.null_to_none(data['length'])
            }

            film = Films(**attributes)
            film.save()
            film.genres = self.get_genres(genres=data['genre_ru'])
            film.countries = self.get_countries(countries=u'Флатландию')
            film.save()
            self.save_trailer(film, data)
            self.save_poster(film, data)
            self.save_actors(film, data)
            self.save_director(film, data)

            return True
        except Exception as ex:
            print('========== {0} =='.format(ex.message))
            print('==============================================')
            print(data.__repr__())
            return False
    def null_to_none(self, value = None):
        if value is None:
            return None
        if value.lower() == 'null':
            return None
        return value

    def film_description(self, data):
        list_desc = [data['description_ru'], data['description_eng']]
        lists = filter(lambda v: ((not v is None) and (v.lower() != u'null')), list_desc)
        return lists[0] if lists else ''

    def film_name(self, data):
        list_names = [data['title_ru'], data['title_eng'], data['title_orig']]
        lists = filter(lambda v: ((not v is None) and (v.lower() != u'null')), list_names)
        return lists[0] if lists else ''

    def film_name_orig(self, data):
        list_names = [data['title_orig'], data['title_eng']]
        lists = filter(lambda v: ((not v is None) and (v.lower() != u'null')), list_names)
        return lists[0] if lists else ''

    def save_trailer(self, film, data = None):
        warnings.warn("Function isn't implemetation")
        pass

    def save_poster(self, film, data = None):
        warnings.warn("Function isn't implemetation")
        pass

    def save_actors(self, film, data = None):
        warnings.warn("Function isn't implemetation")
        pass

    def save_director(self, film, data = None):
        warnings.warn("Function isn't implemetation")
        pass

    def date_or_now(self, date = None):
        if date is None:
            return datetime.datetime.now()
        if self.is_null(date):
            return datetime.datetime.now()
        return datetime.datetime.strptime(date, '%Y-%m-%d')

    def is_null(self, value = None):
        if value is None:
            return true
        return value.lower() == u'NULL'.lower()

    def get_genres(self, genres = None):
        if genres is None:
            return []
        genre_names = map(lambda v: v.strip(), genres.split(','))
        genre_models = []
        for genre_name in genre_names:
            try:
                genre_model = Genres.objects.get(name=genre_name)
            except:
                genre_model = Genres(name=genre_name)
                genre_model.save()

            genre_models.append(genre_model)

        return genre_models

    def get_countries(self, countries = None):
        if countries is None:
            return []
        country_names = map(lambda v: v.strip(), countries.split(','))
        country_models = []
        for country_name in country_names:
            try:
                country_model = Countries.objects.get(name=country_name)
            except:
                country_model = Countries(name=country_name)
                country_model.save()

            country_models.append(country_model)

        return country_models
