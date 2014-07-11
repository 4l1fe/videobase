# coding: utf-8
import gzip
import requests
import StringIO
from itertools import dropwhile
import re
import HTMLParser
import datetime

from apps.films.models import Films
from crawler.constants import RATING_GZIP_FILE_URL

regex = re.compile('[ ]+[.0-9]{10}[ ]+(?P<votes>[0-9]+)[ ]{3}(?P<rating>[0-9][.][0-9])[ ](?P<name>.+)')


def get_rating_source(debug=False):
    output = StringIO.StringIO()
    if debug:
        with open('./crawler/ratings.list.gz') as gf:
            output.write(gf.read())
    else:
        data_request = requests.get(RATING_GZIP_FILE_URL)
        output.write(data_request.content)

    output.seek(0)
    gzf = gzip.GzipFile(fileobj=output)
    return gzf


def dict_gen(line_iter):
    for i, line in enumerate(line_iter):
        match = re.match(regex, line.decode('latin-1'))
        if match:
            yield match.groupdict()


def name_wrapper(dict_list):
    for filmdict in dict_list:
        namestring = filmdict['name']
        name_regex = ('[ ]["](?P<name>[^"]+)["]', '[ ](?P<name>[^(]+)')
        nl = namestring.split()
        di = dropwhile(lambda n: re.match('[(][0-9]{4}[)]', n) is None, nl[::-1])
        try:
            year = next(di)[1:-1]
            name = next((re.sub('[{][^}]+[}]([ ]|\Z)', '', m.groupdict()['name']).strip().lower() for m in (re.match(regex, namestring) for regex in name_regex) if m))
            yield ((year, name), filmdict)
        except StopIteration:
            print u"Couldn't parse name year for {}".format(namestring)


def ny_full_dict(debug=False):
    return dict(name_wrapper(dict_gen(get_rating_source(debug))))


def value_dict_update(year, value):
    value.update({'year': year})
    return value


def process_all():
    '''
    Process all films found in our database and update ratings for them
    if they exist in downloaded file.
    '''
    h = HTMLParser.HTMLParser()
    full_dict = ny_full_dict(False)
    
    name_dict = dict((key[1], value_dict_update(key[0], value)) for key, value in full_dict.items())

    changed_ratings = 0
    fail_years = 0
    for i, film in enumerate(Films.objects.all()):
        key = h.unescape(film.name_orig).lower().strip()
        if len(film.name_orig) < 3:
            continue
        
        if key in name_dict:
            imdb_date = datetime.datetime.strptime(name_dict[key]['year'], "%Y").date()
            changed_ratings += 1
            print u"Found rating for {} ".format(film.name_orig)
            rdict = name_dict[key]
            print "Rating before {} Count before {} ".format(film.rating_imdb, film.rating_imdb_cnt)
            
            film.rating_imdb = 0 if rdict['rating'] is None else rdict['rating']
            film.rating_imdb_cnt = 0 if rdict['votes'] is None else rdict['votes']
            print "Rating after {} Count after {}".format(film.rating_imdb, film.rating_imdb_cnt)
            film.save()
        print "Films ratings found {}".format(changed_ratings)
        print "Films overall {}".format(i+1)