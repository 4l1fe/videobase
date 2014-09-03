# coding: utf-8
from apps.films.models import Films
from crawler.locations_saver import save_location_to_list
from crawler.locrobots import sites_crawler
from crawler.utils.locations_utils import sane_dict, save_location
from videobase.celery import app

__author__ = 'vladimir'


#@app.task(name="process_one_film")
def process_one_film(site, film_id, html_page):
    locations = []
    try:
        film = Films.objects.get(id=film_id)
    except Films.DoesNotExist:
        print "There is no film in db with such id"
        return site, locations
    print "call back ok"
    print "page:", html_page, "dict:", sane_dict, "film", film
    for data in sites_crawler[site]['parser'].parse(html_page, sane_dict, film): # здесь уже по готовому результату парсим
        print u"Trying to put data from %s for %s to db" % (site, unicode(data['film']))
        save_location(**data)
        save_location_to_list(locations, **data)

    return site, locations


def load_and_save_film_page_from_site(site, film_id):
    try:
        film = Films.objects.get(id=film_id)
    except Films.DoesNotExist:
        print "There is no film in db with such id"
        return None
    loaded_data = sites_crawler[site]['loader'](film).load() #загрузка страницы
    saved_file_name = 'site' + '_' + 'film_id_' + str(film.id) + '.html'
    f = open(saved_file_name, 'w')
    f.write(loaded_data['html'])
    f.close()
    print ":ekshdfj"
    return saved_file_name


@app.task(name="load_film_from_site", queue="thor")
def load_film_page_from_site(site, film_id):
    return load_and_save_film_page_from_site(site, film_id)
