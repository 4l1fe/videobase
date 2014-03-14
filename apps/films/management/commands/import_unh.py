import os, csv, re
from datetime import datetime
import codecs
import chardet

from django.db import DatabaseError
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import LabelCommand, BaseCommand, CommandError
from optparse import make_option
from django.db import models
from django.contrib.contenttypes.models import ContentType

from apps.films.models import Films, Genres, Countries

class Command(BaseCommand):
    def __init__(self):
        super(Command, self).__init__()
        self.charset = ''

    def handle(self, *args, **options):
        filename =  args[0]
        if os.path.exists(filename):
            self.stdout.write('Start: Import from UNH CSV from %s' % filename)
            self.import_file( filename)
        else:
            raise Exception('File %s not found' % filename)

    def import_file(self, filename):
        self.stdout.write('Run import -  %s' % filename)
        return self.__csvfile(filename)

    def charset_csv_reader(self, csv_data, dialect=csv.excel,
                           charset='utf-8', **kwargs):
        csv_reader = csv.reader(self.charset_encoder(csv_data, charset),
                                dialect=dialect, **kwargs)
        for row in csv_reader:
            # decode charset back to Unicode, cell by cell:
            yield [unicode(cell, charset) for cell in row]

    def __csvfile(self, datafile):
        """ Detect file encoding and open appropriately """
        filehandle = open(datafile)
        if not self.charset:
            diagnose = chardet.detect(filehandle.read())
            self.charset = diagnose['encoding']
        try:
            csvfile = codecs.open(datafile, 'r', self.charset)
        except IOError:
            self.error('Could not open specified csv file, %s, or it does not exist' % datafile, 0)
        else:
            # CSV Reader returns an iterable, but as we possibly need to
            # perform list commands and since list is an acceptable iterable,
            # we'll just transform it.
            return list(self.charset_csv_reader(csv_data=csvfile,
                                                charset=self.charset))
