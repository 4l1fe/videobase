# coding: utf-8
import json
from crawler.locations_saver import save_location_to_locs_dict
from crawler.tor import simple_tor_get_page
from apps.films.constants import APP_FILM_SERIAL
from crawler.utils.locations_utils import save_location, sane_dict
from apps.films.models import Films


class Amediateka_robot(object):
    def __init__(self):
        pass

    def get_data(self):
        self.get_serials_data()
        self.get_film_data()

    def get_film_data(self):
        search_film_url = '/hbo/api/v1/films.json?'
        site_name = 'www.amediateka.ru'
        filter_film_search = 'limit=1000&offset=0&expand=genres&client_id=amediateka&platform=desktop'
        url = "http://{}{}{}".format(site_name, search_film_url, filter_film_search)
        response = simple_tor_get_page(url)
        data_site = json.loads(response)['films']
        film = Films.objects.values_list('id', 'name')
        data = film.values('name', 'id')
        locations = {
        'info': [],
        'type': 'amediateka_ru'
                }
        for f in data_site:
            for film in data:
                if f['name'] == film['name']:
                    film_data = Films.objects.filter(id=film['id'])
                    for dict_film in film_data:
                        d = self.film_dict(dict_film, f)
                        save_location(**d)
                        save_location_to_locs_dict(locations, **d)
                    break
        return locations

    def get_serials_data(self):
        search_serials_url = '/hbo/api/v1/serials.json?'
        filter_serials_search = 'limit=1000&offset=0&expand=seasons,genres&client_id=amediateka&platform=desktop'
        url = "http://{}{}{}".format('www.amediateka.ru', search_serials_url, filter_serials_search)
        response = simple_tor_get_page(url)
        data_site = json.loads(response)['serials']
        data = Films.objects.values_list('id', 'name').values('name', 'id')
        for s in data_site:
            for serials in data:
                if s['name'] == serials['name']:
                    serials_data = Films.objects.filter(id=serials['id'])
                    for dict_serials in serials_data:
                        if dict_serials.type == APP_FILM_SERIAL:
                            list_serial = self.serial_dict(dict_serials, s)
                            for ser in list_serial:
                                save_location(**ser)
                    break

    def film_dict(self, film, site_film):
        resp_dict = sane_dict(film)
        resp_dict['url_view'] = self.get_film_url(site_film)
        resp_dict['price'] = 0
        resp_dict['type'] = 'amediateka'
        return resp_dict

    def serial_dict(self, serial, site_serial):
        resp_list = []
        for s in site_serial['seasons']:
            resp_dict = sane_dict(serial)
            resp_dict['url_view'] = self.get_serial_url(site_serial, s)
            resp_dict['price'] = 0
            resp_dict['number'] = s['number']
            resp_dict['type'] = 'amediateka'
            resp_list.append(resp_dict)

        return resp_list

    def get_film_url(self, site_film):
        return 'http://www.amediateka.ru/film/' + site_film['id']

    def get_serial_url(self, site_serial, s):
        return 'http://www.amediateka.ru/serial/' + site_serial['id'] + '/' + s['id']



