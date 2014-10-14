# coding: utf-8
from crawler.tasks.locrobots_logging import DebugTask

from crawler.utils.locations_utils import save_location
from videobase.celery import app


__author__ = 'vladimir'


@app.task(name='save_location', queue='location_saver', base=DebugTask)
def save_location_from_robo_task(data):
    return save_location(**data)

