# coding: utf-8
from apps.films.models import Films
from apps.films.models import Persons
from django.contrib.auth.models import User
# import data.film_facts.checker
import data.person_facts.checker
from itertools import chain
import re
import ipdb

LINES_PER_FILE = 50000
ROBOT_FILE = 'interface/static/robots.txt'

FILMS_FILES_PATTERN = 'films_urls{}.txt'
PERSONS_FILES_PATTERN = 'persons_urls{}.txt'
USERS_FILES_PATTERN = 'users_urls{}.txt'

URL_PATTERN = 'http:/vsevi.ru/{}\n'


def file_writer(filename):

    with open(filename,'w') as fw:

        line = 'Debug string'
        while not (line is None):
            line = yield
            if not (line is None):
                fw.write( "Sitemap: {}".format(line))
            
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


def refresh():

    fiter = data_writer(FILMS_FILES_PATTERN ,(URL_PATTERN.format(FILMS_FILES_PATTERN.format(f.id)) for f in Films.objects.all()))
    piter = data_writer(PERSONS_FILES_PATTERN,(URL_PATTERN.format(PERSONS_FILES_PATTERN.format(f.id)) for f in Persons.objects.all()))
    uiter = data_writer(USERS_FILES_PATTERN,(URL_PATTERN.format(USERS_FILES_PATTERN.format(f.id)) for f in User.objects.all()))

    with open(ROBOT_FILE,'r') as rf:
        data = rf.read()
    clean_data = re.sub('Sitemap:[ ]' + URL_PATTERN.format(FILMS_FILES_PATTERN.format('\d')),'',data)
    clean_data = re.sub('Sitemap:[ ]' + URL_PATTERN.format(PERSONS_FILES_PATTERN.format('\d')),'',clean_data)
    clean_data = re.sub('Sitemap:[ ]' + URL_PATTERN.format(USERS_FILES_PATTERN.format('\d')),'',clean_data)
            
        
    with open(ROBOT_FILE,'w') as rf:
        rf.write(clean_data)
        rf.writelines(('Sitemap: '+ s for s in chain(fiter,piter,uiter)))

        