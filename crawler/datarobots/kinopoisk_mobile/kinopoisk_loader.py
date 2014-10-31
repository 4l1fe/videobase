#coding: utf-8
import json
from bs4 import BeautifulSoup
import datetime
from crawler.locrobots.save_util import save_loaded_data_to_file
from crawler.tor import simple_tor_get_page
from apps.films.models import Films
__author__ = 'vladimir'

BASE_URL = 'http://m.kinopoisk.ru/movie/'


class KinopoiskMobile():

    @staticmethod
    def load_all_pages():
        for f in Films.objects.all():
            fn = KinopoiskMobile.load_film_page_to_file(f)
            print "Saved as", fn

    @staticmethod
    def parse_pages_for_all_films():
        for f in Films.objects.all():
            file_name = KinopoiskMobile.load_film_page_to_file(f)
            KinopoiskMobile.process_film_file_page(file_name)

    @staticmethod
    def load_film_page_to_file(film):
        link = BASE_URL + str(film.kinopoisk_id)
        page = simple_tor_get_page(link, True)
        prepared_json = KinopoiskMobile.generate_json(page, link)
        if prepared_json:
            file_name = save_loaded_data_to_file(prepared_json, 'kinopoisk_film_id_{}_date_{}'.format(film.kinopoisk_id, str(datetime.datetime.now().date())), 'kinopoisk_mobile')
        return file_name

    @staticmethod
    def process_film_file_page(film_page_file_name):
        opned_page = open(film_page_file_name)
        json_page = json.load(opned_page)
        beatiful_soup = BeautifulSoup(json_page['html'])

    @staticmethod
    def generate_json(page_content, page_link):
        return {'html': page_content, 'url': page_link}


