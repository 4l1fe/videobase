# coding: utf-8
import json
import os
from apps.contents.models import Locations
from apps.films.models import Films
from crawler.core.exceptions import NoSuchFilm
from crawler.locations_robot_corrector import LocationCorrectorForOneFilmRobots
from crawler.locations_saver import save_location_to_locs_dict
from crawler.locrobots import sites_crawler
from crawler.utils.locations_utils import sane_dict
from crawler.tasks import save_location_from_robo_task

saved_pages_directory = 'saved_pages'


def process_one_film(site, film_id, html_page_json):

    if not html_page_json:
        return
    try:
        film = Films.objects.get(id=film_id)
    except Films.DoesNotExist:
        print "There is no film in db with such id"
        return
    for data in sites_crawler[site]['parser'].parse(html_page_json['html'], sane_dict, film, url=html_page_json['url']): # здесь уже по готовому результату парсим
        data['film'] = film
        try:
            if data['url_view'] == '':
                print "  "
                LocationCorrectorForOneFilmRobots.corrrect_current_location_if_needed(data)
                continue
            print u"Trying to put data from %s for %s to db" % (site, unicode(data['film']))
            save_location_from_robo_task.apply_async((data,))
        except NoSuchFilm:
            print "page parsing failed"




