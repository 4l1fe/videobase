# coding: utf-8
import json
import os
from apps.films.models import Films
from crawler.core.exceptions import NoSuchFilm
from crawler.locations_saver import save_location_to_locs_dict
from crawler.locrobots import sites_crawler
from crawler.utils.locations_utils import sane_dict
from videobase.celery import app
from crawler.tasks.save_location_task import save_location_from_robo_task

__author__ = 'vladimir'

saved_pages_directory = 'saved_pages'


def process_one_film(site, film_id, html_page_json):
    locations = {
        'info': [],
        'type': site
                }
    if not html_page_json:
        return locations
    try:
        film = Films.objects.get(id=film_id)
    except Films.DoesNotExist:
        print "There is no film in db with such id"
        return locations
    for data in sites_crawler[site]['parser'].parse(html_page_json['html'], sane_dict, film, url=html_page_json['url']): # здесь уже по готовому результату парсим
        data['film'] = film
        try:
            print u"Trying to put data from %s for %s to db" % (site, unicode(data['film']))
            save_location_from_robo_task.apply_async((data,))
            status = True
            save_location_to_locs_dict(locations, status, **data)
        except NoSuchFilm:
            print "page parsing failed"
            status = False
            save_location_to_locs_dict(locations, status, **data)
            return locations
    return locations


def save_loaded_data_to_file(loaded_data, film_id, site):
    saved_file_name = 'film_id_' + str(film_id) + '.json'
    try:
        if not os.path.exists(saved_pages_directory):
            os.makedirs(saved_pages_directory)
        site_dir = saved_pages_directory + '/' + site
        if not os.path.exists(site_dir):
            os.makedirs(site_dir)
        f = open(site_dir + '/' + saved_file_name, 'w')
        f.write(json.dumps(loaded_data))
        f.close()
    except:
        return None
    return site_dir + '/' + saved_file_name


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
