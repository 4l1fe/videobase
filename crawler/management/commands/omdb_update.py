from django.core.management.base import NoArgsCommand

import requests
from apps.films.models import Films
import time
import datetime
from crawler.shelved import PersistentDict

class NoResponse(Exception):
    pass
# coding: utf-8

def get_omdb_data(imdb_id):

    time.sleep(5)

    r = requests.get('http://www.omdbapi.com', params={'i':'tt{:07d}'.format(imdb_id)})
    data = r.json()

    if data['Response'] == u'True':
        return data
    else:
        return None

class Command(NoArgsCommand):

    help = u'Refresh date from OMDB data'
    requires_model_validation = True

    def handle_noargs(self, **options):

        
        with PersistentDict('omdb_shelve.json', 'c', format='json') as omdb_shelve:
        
            for film in Films.objects.exclude(imdb_id__isnull=True):

                try:

                    if film.imdb_id in omdb_shelve:
                        data = omdb_shelve[film.imdb_id]
                    else:
                        data = get_omdb_data(film.imdb_id)
                        omdb_shelve[film.imdb_id] = get_omdb_data(film.imdb_id)
                except Exception,e:
                    print e
                
                if data:
                    try:
                        datetime.datetime.strptime(data[u'Released'],"%d %b %Y")
                        print "Updated release date for {}".format(film)
                        film.release_date =  datetime.datetime.strptime(data[u'Released'],"%d %b %Y")

                        film.save()
                    except ValueError, ve:
                        print "Date in unknown format {}".format(data[u'Released'])

                else:
                    print "Skipping {}".format(film)