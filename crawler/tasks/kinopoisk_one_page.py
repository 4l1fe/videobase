# coding: utf-8

from videobase.celery import app
from crawler.datarobots.kinopoisk_ru.kinopoisk import parse_from_kinopoisk


@app.task(name='kinopoisk_parse_film_by_id')
def kinopoisk_parse_one_film(kinopoisk_id_str, name):
    '''
    Task for parsing particual kinopoisk id
    '''

    result_dict = {
        'info': [],
        'type': 'kinopoisk_ru'
    }

    kinopoisk_id = kinopoisk_id_str if type(kinopoisk_id_str) is int else int(kinopoisk_id_str)
    parse_from_kinopoisk(kinopoisk_id=kinopoisk_id, name=name)

    return result_dict

