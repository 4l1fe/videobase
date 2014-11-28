# coding: utf-8
from __future__ import absolute_import
from crawler.casts_robot import parse_sportbox_ru, parse_translation_live_russia_tv, parse_khl, parse_translation_championat_com, parse_ntv_plus_translation
from crawler.casts_robot.cast_utils import save_cast_dict
from videobase.celery import app
from utils.common import traceback_own


def generic_task(parse_function, service_name):
    parsed = parse_function()

    print u'Got {} casts descriptions from {}'.format(len(parsed), service_name)

    for cast_dict in parsed:

        try:
            print u"Trying to save {} cast".format(cast_dict['title'])
            save_cast_dict(service_name, cast_dict)

        except Exception, e:
            traceback_own(e)


@app.task(name='sportbox_update')
def sportbox_update():
    generic_task(parse_sportbox_ru, 'sportbox_ru')


@app.task(name='liverussia_update')
def liverussia_update():
    generic_task(parse_translation_live_russia_tv, 'liverussia_ru')


@app.task(name='championat_update')
def championat_update():
    generic_task(parse_translation_championat_com, 'championat_com')


@app.task(name='khl_update')
def khl_update():
    generic_task(parse_khl, 'khl_ru')


@app.task(name='ntv_plus_update')
def ntv_plus_update():
    generic_task(parse_ntv_plus_translation, 'ntv_plus')