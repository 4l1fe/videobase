from videobase.celery import app
from crawler.kinopoisk import parse_from_kinopoisk


@app.task(name = 'kinopoisk_parse_film_by_id')
def kinopoisk_parse_one_film(kinopoisk_id,name):
    '''
    Task for parsing particual kinopoisk id
    '''
    parse_from_kinopoisk(kinopoisk_id=kinopoisk_id, name = name)
