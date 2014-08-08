# coding: utf-8
from django.core.management.base import NoArgsCommand

import requests
from apps.films.models import Films,Countries
import time
import datetime
from crawler.utils.shelved import PersistentDict

class NoResponse(Exception):
    pass


def get_omdb_data(imdb_id):

    time.sleep(5)

    print "Downloading"
    r = requests.get('http://www.omdbapi.com', params={'i':'tt{:07d}'.format(imdb_id)})
    data = r.json()

    if data['Response'] == u'True':
        return data
    else:
        return None

flatland = Countries.objects.get(name=u'Флатландию')
class Command(NoArgsCommand):

    help = u'Refresh date from OMDB data'
    requires_model_validation = True

    def handle_noargs(self, **options):

        for film in Films.objects.exclude(imdb_id__isnull=True):
            with PersistentDict('omdb_shelve.json', 'c', format='json') as omdb_shelve:
                try:
                    if unicode(film.imdb_id) in omdb_shelve:
                        print "Getting data from shelve"
                        data = omdb_shelve[unicode(film.imdb_id)]
                    else:
                        data = get_omdb_data(film.imdb_id)
                        omdb_shelve[film.imdb_id] = get_omdb_data(film.imdb_id)
                except Exception,e:
                    import traceback
                    traceback.print_exc()
                
                if data:
                    try:
                        datetime.datetime.strptime(data[u'Released'],"%d %b %Y")
                        print "Updated release date for {}".format(film)
                        film.release_date =  datetime.datetime.strptime(data[u'Released'],"%d %b %Y")
                        if flatland in film.countries.all():
                            film.countries.clear()
                            for cname in data['Country'].split(','):
                                try:
                                    country = Countries.objects.get(name_orig =cname)
                                except Countries.DoesNotExist:
                                    country = Countries(name=cname,name_orig=cname,description=' ')
                                    country.save()
                                print "Added {} to countries of {}".format(country,film)
                                film.countries.add(country)
                        film.save()
                    except ValueError, ve:
                        print "Date in unknown format {}".format(data[u'Released'])

                else:
                    print "Skipping {}".format(film)