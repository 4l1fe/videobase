#coding: utf-8
from crawler.datarobots.kinopoisk_mobile.kinopoisk_loader import KinopoiskMobile

__author__ = 'vladimir'
from videobase.celery import app


@app.task(name='kinopoisk_mobile_parse_film')
def kinopoisk_mobile_parse(f_kinopoisk_id, files):
    try:
        max_date_film_fname = KinopoiskMobile.get_max_date_file_name(KinopoiskMobile.load_film_page_to_file, f_kinopoisk_id, files, 3, 5)
        max_date_persons_for_film_fname = KinopoiskMobile.get_max_date_file_name(KinopoiskMobile.load_persons_page_to_file, f_kinopoisk_id, files, 5, 7)
        KinopoiskMobile.process_film_file_page(max_date_film_fname)
        KinopoiskMobile.process_persons_page(max_date_persons_for_film_fname)
    except:
        import traceback
        traceback.print_exc()
