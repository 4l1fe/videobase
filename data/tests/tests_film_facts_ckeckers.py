# coding: utf-8
from datetime import datetime
import os
from PIL import Image
from django.core.files import File
from apps.films.constants import APP_PERSON_DIRECTOR, APP_PERSON_PRODUCER
from apps.films.tests.factories import FilmFactory, FilmsExtrasFactory, CountriesFactory, PersonsFilmFactory
from data.constants import FLATLAND_NAME
from data.film_facts.checker import is_trailer_contains_film_name, is_trailer_match_key_words, is_size_of_photo_ok, \
    is_flatland_in_countries, is_trailer_duration_ok, is_kinopoisk_id_set, is_trailer_release_date_is_2014, \
    is_film_no_name, is_film_description_contains_html, is_film_description_contains_digits, \
    is_film_description_contains_useless_site_names, is_kinopoisk_rating_set, is_script_writer_ok, \
    is_produced_country_in_english, is_omdb_year_differs_more_than_year, is_trailer_exists
from data.film_facts.trailer_title_check import is_correct_trailer_title

__author__ = 'vladimir'

import unittest


class TestFilmFactsCheckersWithGoodData(unittest.TestCase):

    def setUp(self):
        self.countries = []
        self.films = []
        self.film_extras = []
        self.persons_film = []
        self.countries.append(CountriesFactory.create(name=u'Россия'))
        self.countries.append(CountriesFactory.create(name=u'Франция'))
        self.films.append(FilmFactory.create(release_date=datetime.strptime('2014', '%Y'), countries=(self.countries[0], self.countries[1]),
                                             kinopoisk_id=12121, name=u'Иллюзия обмана', description=u'Описание фильма Иллюзия обмана', rating_kinopoisk=5))

        self.film_extras.append(FilmsExtrasFactory.create(film=self.films[-1]))
        self.film_extras[-1].photo.save(self.create_big_image(), File(open(self.create_big_image(), mode="rb")))
        self.film_extras[-1].url = u'http://www.youtube.com/watch?v=uUPV6oFIXgw'

        self.persons_film.append(PersonsFilmFactory.create(film=self.films[-1], p_type=APP_PERSON_DIRECTOR))

    def create_big_image(self):
        tst_photo_name = 'tmp_test_photo.jpg'
        size = (2100, 2200)
        im = Image.new('RGB', size)
        im.save("tmp_test_photo.jpg")
        return tst_photo_name

    def tearDown(self):
        os.remove("tmp_test_photo.jpg")

    def test_is_flatland_in_countries(self):
        self.assertEqual(is_flatland_in_countries(self.films[-1]), False)

    def test_is_trailer_contains_film_name(self):
        self.assertEqual(is_trailer_contains_film_name(self.films[-1], self.film_extras[-1]), True)

    def test_is_omdb_year_differs_more_than_year(self):
        self.assertEqual(is_omdb_year_differs_more_than_year(self.films[-1]), False)

    def test_is_trailer_exists(self):
        self.assertEqual(is_trailer_exists(self.film_extras[-1]), True)

    def test_is_trailer_duration_ok(self):
        self.assertEqual(is_trailer_duration_ok(self.film_extras[-1]), True)

    def test_is_trailer_release_date_is_2014(self):
        self.assertEqual(is_trailer_release_date_is_2014(self.films[-1]), True)

    def test_is_kinopoisk_id_set(self):
        self.assertEqual(is_kinopoisk_id_set(self.films[-1]), True)

    def test_is_film_no_name(self):
        self.assertEqual(is_film_no_name(self.films[-1]), False)

    def test_is_film_description_contains_html(self):
        self.assertEqual(is_film_description_contains_html(self.films[-1]), False)

    def test_is_film_description_contains_digits(self):
        self.assertEqual(is_film_description_contains_digits(self.films[-1]), False)

    def test_is_film_description_contains_useless_site_names(self):
        self.assertEqual(is_film_description_contains_useless_site_names(self.films[-1]), False)

    def test_is_kinopoisk_rating_set(self):
        self.assertEqual(is_kinopoisk_rating_set(self.films[-1]), True)

    def test_is_script_writer_ok(self):
        self.assertEqual(is_script_writer_ok(self.persons_film[-1]), True)

    def test_is_produced_country_in_english(self):
        self.assertEqual(is_produced_country_in_english(self.films[-1]), False)

    def test_is_trailer_match_key_words(self):
        self.assertEqual(is_trailer_match_key_words(self.films[-1], self.film_extras[-1]), False)

    def test_is_size_of_photo_ok(self):
        self.assertEqual(is_size_of_photo_ok(self.film_extras[-1]), True)

    def test_is_correct_trailer_title(self):
        print self.films[-1]
        self.assertEqual(is_correct_trailer_title(u'Иллюзия обмана 2014 русский трейлер', self.films[-1]), True)


class TestFilmFactsCheckersWithBadData(unittest.TestCase):

    def setUp(self):
        self.countries = []
        self.films = []
        self.film_extras = []
        self.persons_film = []
        self.countries.append(CountriesFactory.create(name=u'Россия'))
        self.countries.append(CountriesFactory.create(name=u'USA'))
        self.countries.append(CountriesFactory.create(name=FLATLAND_NAME))
        self.films.append(FilmFactory.create(release_date=datetime.strptime('2010', '%Y'), countries=(self.countries[0], self.countries[1], self.countries[2]),
                                             kinopoisk_id=0, name=u'NoName', description=u'Описание фильма  34 <br> 454  NOW.RU', rating_kinopoisk=0))

        self.film_extras.append(FilmsExtrasFactory.create(film=self.films[-1]))
        self.film_extras[-1].photo.save(self.create_small_image(), File(open(self.create_small_image(), mode="rb")))
        self.film_extras[-1].url = u'http://www.youtube.com/watch?v=uUPV6oFI11111'

        self.persons_film.append(PersonsFilmFactory.create(film=self.films[-1], p_type=APP_PERSON_PRODUCER))

    def create_small_image(self):
        tst_photo_name = 'tmp_test_photo.jpg'
        size = (100, 200)
        im = Image.new('RGB', size)
        im.save("tmp_test_photo.jpg")
        return tst_photo_name

    def tearDown(self):
        os.remove("tmp_test_photo.jpg")

    def test_is_flatland_in_countries(self):
        self.assertEqual(is_flatland_in_countries(self.films[-1]), True)

    def test_is_trailer_contains_film_name(self):
        self.assertEqual(is_trailer_contains_film_name(self.films[-1], self.film_extras[-1]), True)

    def test_is_omdb_year_differs_more_than_year(self):
        self.assertEqual(is_omdb_year_differs_more_than_year(self.films[-1]), False)

    def test_is_trailer_exists(self):
        self.assertEqual(is_trailer_exists(self.film_extras[-1]), False)

    def test_is_trailer_duration_ok(self):
        self.assertEqual(is_trailer_duration_ok(self.film_extras[-1]), True)

    def test_is_trailer_release_date_is_2014(self):
        self.assertEqual(is_trailer_release_date_is_2014(self.films[-1]), False)

    def test_is_kinopoisk_id_set(self):
        self.assertEqual(is_kinopoisk_id_set(self.films[-1]), False)

    def test_is_film_no_name(self):
        self.assertEqual(is_film_no_name(self.films[-1]), True)

    def test_is_film_description_contains_html(self):
        self.assertEqual(is_film_description_contains_html(self.films[-1]), True)

    def test_is_film_description_contains_digits(self):
        self.assertEqual(is_film_description_contains_digits(self.films[-1]), True)

    def test_is_film_description_contains_useless_site_names(self):
        self.assertEqual(is_film_description_contains_useless_site_names(self.films[-1]), True)

    def test_is_kinopoisk_rating_set(self):
        self.assertEqual(is_kinopoisk_rating_set(self.films[-1]), False)

    def test_is_script_writer_ok(self):
        self.assertEqual(is_script_writer_ok(self.persons_film[-1]), False)

    def test_is_produced_country_in_english(self):
        self.assertEqual(is_produced_country_in_english(self.films[-1]), True)

    def test_is_trailer_match_key_words(self):
        self.assertEqual(is_trailer_match_key_words(self.films[-1], self.film_extras[-1]), True)

    def test_is_size_of_photo_ok(self):
        self.assertEqual(is_size_of_photo_ok(self.film_extras[-1]), False)

    def test_is_correct_trailer_title(self):
        self.assertEqual(is_correct_trailer_title(u'Трейлер для фильма 2014',self.films[-1]), False)