# coding: utf-8

from apps.films.models import Persons
import datetime
import time
import gzip

process_line_tuple = lambda des : (des[0].split('/')[-1].split('>')[0],des[2].split('"')[1])


def open_dbpedia_file(filepath):

    with gzip.open(filepath) as tfile:
        for line in tfile.readlines():
            if 'birthDate' in line:
                yield process_line_tuple(line.split())


def update_birthdates_from_dbpedia(processed_lines):

    name_births = dict(processed_lines)
    dbpedia_names = name_births.keys()

    videobase_names = [(p,p.name_orig.replace(' ','_'))
                   if p.name_orig
                   else (p,p.name.replace(' ','_'))
                   for p in  Persons.objects.all()]

    shared = set(dbpedia_names).intersection(p[1] for p in videobase_names)

    for person,videobase_name in videobase_names:

        if videobase_name in shared:
            try:
                new_birthdate = datetime.datetime.strptime(name_births[videobase_name],"%Y-%m-%d")
                print "Birthdate of {} before {}, after {} updating".format(person,person.birthdate,new_birthdate) 
                person.birthdate = new_birthdate
                person.save()
            except ValueError as ve:
                print "Couldn't parse {} for {}".format(name_births[videobase_name],videobase_name)
                


