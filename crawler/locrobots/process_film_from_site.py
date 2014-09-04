# coding: utf-8

from crawler.locrobots.process_films_tasks import *

__author__ = 'vladimir'


def get_html_json_for_file_name(file_name):
    f = open(file_name, 'r')
    print file_name
    raw_text = f.read()
    html = json.loads(raw_text)
    f.close()
    return html


def process_film_on_site(site, film_id):
    result = load_film_page_from_site.apply_async((site, film_id))
    html_file_name = result.get(propagate=False)
    html_json = get_html_json_for_file_name(html_file_name)
    return process_one_film(site, film_id, html_json)


