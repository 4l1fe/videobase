# coding: utf-8
import json
import os
from apps.films.models import Films
from crawler.core.exceptions import NoSuchFilm
from crawler.locations_saver import save_location_to_locs_dict
from crawler.locrobots import sites_crawler
from crawler.utils.locations_utils import sane_dict
from crawler.tasks import save_location_from_robo_task

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
            if data['url_view'] == '':
                continue
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



