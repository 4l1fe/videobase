# coding: utf-8
import json
from apps.films.models import Films
from crawler.core.exceptions import NoSuchFilm
from crawler.locations_saver import save_location_to_list
from crawler.locrobots import sites_crawler
from crawler.utils.locations_utils import sane_dict, save_location
from videobase.celery import app

__author__ = 'vladimir'


#@app.task(name="process_one_film")
def process_one_film(site, film_id, html_page_json):
    locations = []
    if not html_page_json:
        return site, locations
    try:
        film = Films.objects.get(id=film_id)
    except Films.DoesNotExist:
        print "There is no film in db with such id"
        return site, locations
    try:
        for data in sites_crawler[site]['parser'].parse(html_page_json['html'], sane_dict, film, url=html_page_json['url']): # здесь уже по готовому результату парсим
            print u"Trying to put data from %s for %s to db" % (site, unicode(data['film']))
            save_location(**data)
            save_location_to_list(locations, **data)
    except NoSuchFilm:
        print "page parsing failed"
        return site, locations
    return site, locations


def save_loaded_data_to_file(loaded_data, film_id, site):
    saved_file_name = site + '_' + 'film_id_' + str(film_id) + '.html'
    try:
        f = open(saved_file_name, 'w')
        f.write(json.dumps(loaded_data))
        f.close()
    except:
        return None
    return saved_file_name


def load_and_save_film_page_from_site(site, film_id):
    try:
        film = Films.objects.get(id=film_id)
    except Films.DoesNotExist:
        print "There is no film in db with such id"
        return None
    try:
        loaded_data = sites_crawler[site]['loader'](film).load() #загрузка страницы
        saved_file_name = save_loaded_data_to_file(loaded_data, film.id, site)
    except NoSuchFilm:
        print "page loading failed"
        return None
    return saved_file_name


@app.task(name="load_film_from_site", queue="thor")
def load_film_page_from_site(site, film_id):
    return load_and_save_film_page_from_site(site, film_id)
