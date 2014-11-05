# coding: utf-8

__author__ = 'vladimir'


def create_location_result(location_type, location_id, film_id, status, is_new):
    loc_dict = {'location_type': location_type,
                'location_id': location_id,
                'film_id': film_id,
                'status': status,
                'is_new': is_new
                }
    return loc_dict
