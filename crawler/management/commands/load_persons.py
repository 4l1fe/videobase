# coding: utf-8
from django.core.management.base import NoArgsCommand

from apps.films.models import Persons
from videobase.settings import BASE_DIR

import json
import os


class Command(NoArgsCommand):

    def handle_noargs(self, **options):
        path = os.path.join(BASE_DIR, 'sparql.json')
        js_data = ''
        with open(path, 'r') as fd:
           js_data = json.load(fd)
        js_persons = js_data['results']['bindings']
        for js_person in js_persons:
            name = js_person['ru_name']['value'].split(',')
            name = u'{} {}'.format(name[-1], name[0])
            name_orig = js_person['en_name']['value']
            try:
                person = Persons.objects.get(name_orig=name_orig, name=name_orig)
                person.name = name
                person.save()
            except Exception as e:
                # print e
                pass
