# coding: utf-8
from crawler.datarobots.kinopoisk_ru.parse_page import convert_file

__author__ = 'vladimir'

import json
import os
import time
import requests
from requests.exceptions import ConnectionError


def get_one_google_image_by_query(query, path=''):
    BASE_URL = 'https://ajax.googleapis.com/ajax/services/search/images?'\
    'v=1.0&q=' + query + '&start=%d'

    BASE_PATH = os.path.join(path, 'static/upload/castextras')
    if not os.path.exists(BASE_PATH):
        os.makedirs(BASE_PATH)
    is_first_image_saved = False
    start = 0 # Google's start query string parameter for pagination.
    while start < 7: # Google will only return a max of 56 results.
        r = requests.get(BASE_URL % start)
        try:
            for image_info in json.loads(r.text)['responseData']['results']:
                try:
                    url = image_info['unescapedUrl']
                    image_r = requests.get(url)
                    # Remove file-system path characters from name.
                    title = image_info['titleNoFormatting'].replace('/', '').replace('\\', '')
                    if len(title) > 50:
                        title = title[:50]
                    fle = convert_file(image_r.content)
                    is_first_image_saved = True

                except ConnectionError, e:
                    print 'could not download %s' % url
                    continue
                except IOError, e:
                    print 'could not save %s' % url
                    print e.message
                    continue
                except Exception, e:
                    print "WARNING", e.message
                    continue
                if is_first_image_saved:
                    return fle
        except Exception, e:
            continue

        start += 4 # 4 images per page.
        # Be nice to Google and they'll be nice back :)
        time.sleep(1.5)
