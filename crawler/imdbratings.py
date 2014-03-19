import re
import gzip
import requests
import StringIO
from crawler.constants import RATING_GZIP_FILE_URL
from itertools import dropwhile
import re
import logging


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

    for i,line in enumerate(line_iter):
        match = re.match(regex, line.decode('latin-1'))
        if match:
            yield match.groupdict()

def name_wrapper(dict_list):

    for filmdict in dict_list:
        namestring = filmdict['name']
        name_regex = ('[ ]["](?P<name>[^"]+)["]','[ ](?P<name>[^(]+)')
        nl = namestring.split()
        di = dropwhile(lambda n: re.match('[(][0-9]{4}[)]',n) is None,nl[::-1])
        try:
            year = next(di)[1:-1]
            name = next((re.sub('[{][^}]+[}]([ ]|\Z)','',m.groupdict()['name']).strip().lower() for m in (re.match(regex,namestring) for regex in name_regex) if m ))
            yield ((year, name),filmdict)
        except StopIteration:
            logging.debug(u"Couldn't parse name year for {}".format(namestring).encode('utf-8'))

def ny_full_dict(debug=False):
    return dict(name_wrapper(dict_gen(get_rating_source(debug))))

