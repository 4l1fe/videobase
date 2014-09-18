# coding: utf-8
from crawler.locrobots.save_util import load_and_save_film_page_from_site
from videobase.celery import app

__author__ = 'vladimir'


@app.task(name="load_film_from_site", queue="thor")
def load_film_page_from_site(site, film_id):
    return load_and_save_film_page_from_site(site, film_id)