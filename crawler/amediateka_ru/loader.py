# coding: utf-8
import json
import requests
from apps.films.constants import APP_FILM_SERIAL
from crawler.robot_start import save_location, sane_dict
from apps.films.models import Films


class Amediateka_robot(object):
    def __init__(self):
        pass

    def get_data(self):
        self.get_serials_data()
        self.get_film_data()

    def get_film_data(self):
        search_film_url = '/hbo/api/v1/films.json?'
        filter_film_search = 'limit=1000&offset=0&expand=genres&client_id=amediateka&platform=desktop'
        url = "http://%s%s%s" % ('www.amediateka.ru', search_film_url, filter_film_search)
        response = requests.get(url)
        data_site = json.loads(response.content)['films']
        film = Films.objects.values_list('id', 'name')
        data = film.values('name', 'id')
        for f in data_site:
            for film in data:
                if f['name'] == film['name']:
                    film_data = Films.objects.filter(id=film['id'])
                    for dict_film in film_data:
                        d = self.film_dict(dict_film, f)
                        save_location(**d)
                    continue

    def get_serials_data(self):
        search_serials_url = '/hbo/api/v1/serials.json?'
        filter_serials_search = 'limit=1000&offset=0&expand=seasons,genres&client_id=amediateka&platform=desktop'
        url = "http://%s%s%s" % ('www.amediateka.ru', search_serials_url, filter_serials_search)
        response = requests.get(url)
        data_site = json.loads(response.content)['serials']
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
                    continue

    def film_dict(self, film, site_film):
        resp_dict = sane_dict(film)
        resp_dict['url_view'] = self.get_film_url(site_film)
        resp_dict['price'] = 0
        return resp_dict

    def serial_dict(self, serial, site_serial):
        resp_list = []
        for s in site_serial['seasons']:
            resp_dict = sane_dict(serial)
            resp_dict['url_view'] = self.get_serial_url(site_serial, s)
            resp_dict['price'] = 0
            resp_dict['number'] = s['number']
            resp_list.append(resp_dict)

        return resp_list

    def get_film_url(self, site_film):
        return 'http://www.amediateka.ru/film/' + site_film['id']

    def get_serial_url(self, site_serial, s):
        return 'http://www.amediateka.ru/serial/' + site_serial['id'] + '/' + s['id']



