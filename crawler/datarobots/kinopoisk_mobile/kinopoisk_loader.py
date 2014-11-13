#coding: utf-8
import json
import os
from time import sleep
from bs4 import BeautifulSoup
import datetime
import re
import requests
from apps.films.constants import APP_PERSON_PRODUCER, APP_PERSON_ACTOR, APP_PERSON_DIRECTOR, APP_PERSON_SCRIPTWRITER, \
    APP_FILM_FULL_FILM, APP_FILM_SERIAL
from crawler.datarobots.kinopoisk_ru.kinopoisk import get_country, get_genre
from crawler.locrobots.save_util import save_loaded_data_to_file
from crawler.tor import simple_tor_get_page
from apps.films.models import Films, PersonsFilms, Persons

__author__ = 'vladimir'

BASE_FILM_URL = 'http://m.kinopoisk.ru/movie/'
BASE_PERSONS_URL = 'http://m.kinopoisk.ru/cast/'


class KinopoiskMobile():

    @staticmethod
    def update_all_from_kinopoisk():
        i = 1
        while i < 999999:
            fn = KinopoiskMobile.load_film_page_to_file(i)
            sleep(1)
            per_f = KinopoiskMobile.load_persons_page_to_file(i)
            sleep(2) #чтобы не палиться на киопоиске
            i+=1
        KinopoiskMobile.parse_pages_for_all_files_in_dir()

    @staticmethod
    def load_all_pages():
        for f in Films.objects.all():
            fn = KinopoiskMobile.load_film_page_to_file(f.kinopoisk_id)
            per_f = KinopoiskMobile.load_persons_page_to_file(f.kinopoisk_id)

    @staticmethod
    def parse_pages_for_all_files_in_dir():
        json_path = 'saved_pages/kinopoisk_mobile/'
        files = os.listdir(json_path)
        for file in files:
            if 'persons' not in file:
                print file
                KinopoiskMobile.process_film_file_page(json_path + file)
        for file in files:
            if 'persons' in file:
                print file
                KinopoiskMobile.process_persons_page(json_path + file)


    @staticmethod
    def parse_pages_for_all_films():
        json_path = 'saved_pages/kinopoisk_mobile/'
        files = os.listdir(json_path)
        for f in Films.objects.all():
            max_date_film_fname = KinopoiskMobile.get_max_date_file_name(KinopoiskMobile.load_film_page_to_file, f.kinopoisk_id, files, 3, 5)
            max_date_persons_for_film_fname = KinopoiskMobile.get_max_date_file_name(KinopoiskMobile.load_persons_page_to_file, f.kinopoisk_id, files, 5, 7)
            KinopoiskMobile.process_film_file_page(max_date_film_fname)
            KinopoiskMobile.process_persons_page(max_date_persons_for_film_fname)

    @staticmethod
    def get_max_date_file_name(load_func, f_kinopoisk_id, files, k_id_index, date_index):
        max_date_fname = ''
        max_date = None
        for file_name in files:
            attrs = file_name.split('_')
            if attrs[k_id_index] == str(f_kinopoisk_id):
                file_date = datetime.datetime.strptime(attrs[date_index].split('.')[0], '%Y-%m-%d')
                if not max_date or file_date >max_date:
                    max_date = file_date
                    max_date_fname = file_name
        if max_date_fname == '':
            max_date_fname = load_func(f_kinopoisk_id)
            print "Page(pesr page) for film {} will be downloaded".format(f_kinopoisk_id)
        else:
            max_date_fname = 'saved_pages/kinopoisk_mobile/' + max_date_fname
            print "Found local page for film {}".format(f_kinopoisk_id)
        return  max_date_fname

    @staticmethod
    def load_film_page_to_file(f_kinopoisk_id):
        file_name = None
        link = BASE_FILM_URL + str(f_kinopoisk_id)
        page = simple_tor_get_page(link, True)
        if not KinopoiskMobile.is_film_page(page):
            return None
        print "That's film page"
        page = page.decode(encoding='cp1251')
        prepared_json = KinopoiskMobile.generate_json(page, link)
        if prepared_json:
            file_name = save_loaded_data_to_file(prepared_json, 'kinopoisk_film_id_{}_date_{}'.format(f_kinopoisk_id, str(datetime.datetime.now().date())), 'kinopoisk_mobile')
            print "Saved film page as {}".format(file_name)
        return file_name

    @staticmethod
    def load_persons_page_to_file(f_kinopoisk_id):
        file_name = None
        link = BASE_PERSONS_URL + str(f_kinopoisk_id)
        page = simple_tor_get_page(link, True)
        if not KinopoiskMobile.is_film_page(page):
            return None
        page = page.decode(encoding='cp1251')
        prepared_json = KinopoiskMobile.generate_json(page, link)
        if prepared_json:
            file_name = save_loaded_data_to_file(prepared_json, 'kinopoisk_persons_for_film_id_{}_date_{}'.format(f_kinopoisk_id, str(datetime.datetime.now().date())), 'kinopoisk_mobile')
            print "Saved film persons page as {}".format(file_name)
        return file_name

    @staticmethod
    def process_persons_page(persons_page_file_name):
        with open(persons_page_file_name) as opened_page:
            json_page = json.load(opened_page, encoding='cp1251')
            beatiful_soup = BeautifulSoup(json_page['html'])
            film_actors_parser = ParseFilmActors(beatiful_soup)
            persons = film_actors_parser.get_film_actors()
            k_id = int(persons_page_file_name.split('/')[2].split('_')[5])
            films = Films.objects.filter(kinopoisk_id=k_id)
            if len(films) == 0:
                return
            for key, value in persons.iteritems():
                for actor in value:
                    persn = ParseFilmActors.get_person(actor['name'], actor['link'].split('/')[4])
                    pers_films = ParseFilmActors.save_persons_films(films[0], persn, actor['type'])


    @staticmethod
    def is_film_page(page):
        beatiful_soup = BeautifulSoup(page)
        p = beatiful_soup.find('p', {"class": "title"})
        if p:
            return True
        else:
            return False

    @staticmethod
    def process_film_file_page(film_page_file_name):
        with open(film_page_file_name) as opened_page:
            json_page = json.load(opened_page, encoding='cp1251')
            beatiful_soup = BeautifulSoup(json_page['html'])
            one_parsed_page = ParseOneKinopoiskMobilePage(beatiful_soup)
            k_id = int(film_page_file_name.split('/')[2].split('_')[3])
            name = one_parsed_page.get_name()
            if not name:
                return
            film = KinopoiskMobile.get_film(k_id, name)

            year = one_parsed_page.get_year()
            if year:
                film.release_date = datetime.datetime.strptime(year, '%Y')

            description = one_parsed_page.get_descrition()
            if description:
                film.description = description

            name_orig = one_parsed_page.get_orig_name()
            if name_orig:
                film.name_orig = name_orig
            for genre_name in one_parsed_page.get_genres():
                if genre_name != u'' and not genre_name in film.genres.all():
                    genre = get_genre(genre_name)
                    film.genres.add(genre)

            for country_name in one_parsed_page.get_produced_countries():
                if country_name != u'' and not country_name in film.countries.all():
                    country = get_country(country_name)
                    film.countries.add(country)

            rating_kinopoisk, rating_kinopoisk_cnt = one_parsed_page.get_kinopoisk_rating()
            if rating_kinopoisk:
                film.rating_kinopoisk = rating_kinopoisk
            if rating_kinopoisk_cnt:
                film.rating_imdb_cnt = rating_kinopoisk_cnt

            rating_imdb, rating_imdb_cnt = one_parsed_page.get_imdb_rating()
            if rating_imdb:
                film.rating_imdb = rating_imdb
            if rating_imdb_cnt:
                film.rating_imdb_cnt = rating_imdb_cnt

            f_type = one_parsed_page.get_type()
            if f_type:
                film.type = f_type
                if f_type == APP_FILM_SERIAL:
                    film.name = film.name.replace(u'(сериал)','')
            film.save()
            print "#Parsed: ", one_parsed_page.get_name(),\
                one_parsed_page.get_type(),\
                one_parsed_page.get_orig_name(),\
                one_parsed_page.get_year(),\
                one_parsed_page.get_genres(),\
                one_parsed_page.get_produced_countries(),\
                one_parsed_page.get_descrition(),\
                one_parsed_page.get_kinopoisk_rating(),\
                one_parsed_page.get_imdb_rating(),\
                one_parsed_page.get_duration()

    @staticmethod
    def get_film(kinopoisk_id, name):
        films = Films.objects.filter(kinopoisk_id=kinopoisk_id)
        if len(films) > 0:
            film = films[0]
        else:
            film = Films(name=name, kinopoisk_id=kinopoisk_id)
            film.save()
        return film

    @staticmethod
    def generate_json(page_content, page_link):
        return {'html': page_content, 'url': page_link}


class ParseOneKinopoiskMobilePage():
    def __init__(self, bs_content):
        self.page = bs_content

    def get_name(self):
        res = ''
        try:
            p = self.page.find('p', {"class": "title"})
            res = p.find('b').text
        except Exception, e:
            pass
        return res

    def get_type(self):
        res = APP_FILM_FULL_FILM
        try:
            p = self.page.find('p', {"class": "title"})
            if u'(сериал)' in p.find('b').text:
                res = APP_FILM_SERIAL
        except Exception, e:
            pass
        return res

    def get_orig_name(self):
        res = ''
        try:
            p = self.page.find('p', {"class": "title"})
            res = p.find('span').text.split(',')[0]
        except Exception, e:
            pass
        return res

    def get_year(self):
        res = None
        p = self.page.find('p', {"class": "title"})
        try:
            res = p.find('span').text.split(',')[1].replace(' ','')
            if len(res) != 4:
                return None
        except Exception, e:
            pass
        return res

    def get_descrition(self):
        res = ''
        try:
            div = self.page.find('div', {"class": "block film"})
            res = div.find('p', {"class": "descr"}).text
        except Exception, e:
            pass
        return res

    def get_produced_countries(self):
        res = []
        try:
            div = self.page.find('div', {"class": "block film"})
            res = div.findAll('span')[1].text.split(',')
        except Exception, e:
            pass
        return res

    def get_genres(self):
        res = []
        try:
            div = self.page.find('div', {"class": "block film"})
            res = div.findAll('span')[0].text.split(',')
        except Exception, e:
            pass
        return res

    def get_kinopoisk_rating(self):
        try:
            div = self.page.find('div', {"class": "block film"})
            spans = div.findAll('span')
            for sp in spans:
                i_tags = sp.findAll('i')
                if len(i_tags) >= 2:
                    count = int(re.sub("\D", "", sp.contents[4]))
                    return i_tags[0].text, count
        except Exception, e:
            import traceback
            traceback.print_exc()
        return 0, 0

    def get_imdb_rating(self):
        try:
            div = self.page.find('div', {"class": "block film"})
            spans = div.findAll('span')
            for sp in spans:
                i_tags = sp.findAll('i')
                if len(i_tags) >= 2:
                    count = int(re.sub("\D", "", sp.contents[10]))
                    return i_tags[1].text, count
        except Exception, e:
            import traceback
            traceback.print_exc()
        return 0, 0

    def get_budget(self):
        res = None
        p = self.page.find('p', {"class": "title"})
        try:
            res = p.find('span').text.split(',')[2].replace(' ','')
        except Exception, e:
            pass
        return res

    def get_duration(self):
        res = None
        p = self.page.find('p', {"class": "title"})
        try:
            res = p.find('span').text.split(',')[2].replace(' ','')
            res = int(re.sub("\D", "", res))
        except Exception, e:
            pass
        return res


class ParseFilmActors():

    def __init__(self, bs_content):
        self.page = bs_content
        self.types = {
            u"Режиссеры": APP_PERSON_DIRECTOR,
            u"Актеры": APP_PERSON_ACTOR,
            u"Продюсеры": APP_PERSON_PRODUCER,
            u"Сценаристы":APP_PERSON_SCRIPTWRITER
        }

    def get_film_actors(self):
        try:
            block = self.page.find('dl', { "class" : "block"})
            p_type = None
            index = 0
            persons = {}
            for cont in block.contents:
                if 'dt' == cont.name:
                    p_type = cont.text
                if 'dd' == cont.name:
                    if p_type not in self.types:
                        continue
                    simple_person = {
                        'name': cont.find('a').text,
                        'link': cont.find('a')['href'],
                        'type': self.types[p_type],
                        'index': index
                    }
                    if p_type in persons:
                        persons[p_type] += [simple_person]
                        index += 1
                    else:
                        persons[p_type] = [simple_person]
                        index += 1
        except Exception, e:
            pass
        return persons

    @staticmethod
    def save_persons_films(film, person, pers_type): #p_index
        person_films = PersonsFilms.objects.filter(film=film, person=person, p_type=pers_type)
        if person_films.count() == 0:
            msg = u"Adding link for film {film} and person {person}"
            print msg.format(film=film, person=person)
            person_film = PersonsFilms(person=person, film=film, p_type=pers_type)
            person_film.save()
        # else:
        #     person_films[0].p_index = p_index
        #     person_films[0].save()


    @staticmethod
    def get_person(name, kinopoisk_id):
        persons = Persons.objects.filter(kinopoisk_id=kinopoisk_id)
        if persons.count() == 0:
            person = Persons(name=name, photo='', kinopoisk_id=kinopoisk_id)
            person.save()
            print u'Added Person {name}'.format(name=name)
        else:
            person = persons[0]
        return person






