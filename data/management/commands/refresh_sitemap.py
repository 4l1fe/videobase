# coding: utf-8
from django.core.management.base import NoArgsCommand
from apps.films.models import Films
from apps.films.models import Persons
# import data.film_facts.checker
import data.person_facts.checker
from itertools import chain
import re
import ipdb

LINES_PER_FILE = 10000
ROBOT_FILE = 'robots.txt'

FILMS_FILES_PATTERN = 'films_urls{}.txt'
PERSONS_FILES_PATTERN = 'persons_urls{}.txt'

URL_PATTERN = 'http:/vsevi.ru/{}\n'

class StopSignal(object):
    pass

def file_writer(filename):

    with open(filename,'w') as fw:

        line = 'Debug string'
        while not (line is None):
            line = yield
            if not (line is None):
                fw.write( "{}\n".format(line))
            
    yield None

def data_writer(file_template, source):

    fw = None
    for count, element in enumerate(source):


        # Refreshing (or creating) file.
        if count % LINES_PER_FILE == 0:
            if fw:
                fw.send(None)

            fw = file_writer(file_template.format(count // LINES_PER_FILE))
            yield URL_PATTERN.format(file_template.format(count // LINES_PER_FILE))
            next(fw)

        fw.send(element)



class Command(NoArgsCommand):
    def handle_noargs(self, **options):

        fiter = data_writer(FILMS_FILES_PATTERN ,(URL_PATTERN.format(FILMS_FILES_PATTERN.format(f.id)) for f in Films.objects.all()))
        piter = data_writer(PERSONS_FILES_PATTERN,(URL_PATTERN.format(PERSONS_FILES_PATTERN.format(f.id)) for f in Persons.objects.all()))

        with open(ROBOT_FILE,'r') as rf:
            data = rf.read()
        clean_data = re.sub(URL_PATTERN.format(FILMS_FILES_PATTERN.format('\d')),'',data)
        clean_data = re.sub(URL_PATTERN.format(PERSONS_FILES_PATTERN.format('\d')),'',clean_data)
            
        
        with open(ROBOT_FILE,'w') as rf:
            rf.write(clean_data)
            rf.writelines(chain(fiter,piter))

