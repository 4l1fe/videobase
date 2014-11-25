# coding: utf-8

__author__ = 'vladimir'

from crawler.locrobots.process_film_from_site import process_film_on_site
from crawler.tasks.locrobots_logging import DebugTask
from videobase.celery import app


@app.task(name='process_individual_film_on_site')
def process_individual_film_on_site(site, film_id, url=None):
    process_film_on_site(site, film_id, url)