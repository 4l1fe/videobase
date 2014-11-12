# coding: utf-8

from django.core.management.base import NoArgsCommand

from crawler.various.birthdates_dbpedia import update_birthdates_from_dbpedia, open_dbpedia_file

DBPEDIA_PERSON_TRIPLES_FILE = 'persondata_en.nt.gz'


class Command(NoArgsCommand):

    def handle_noargs(self, **options):
        update_birthdates_from_dbpedia(open_dbpedia_file(DBPEDIA_PERSON_TRIPLES_FILE))