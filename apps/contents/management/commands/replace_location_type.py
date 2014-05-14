# coding: utf-8

import sys
import traceback
from urllib2 import urlparse
from time import time

from django.db import transaction
from django.core.management.base import BaseCommand, CommandError

from apps.contents.models import Locations
from apps.contents.constants import APP_CONTENTS_LOC_TYPE


class Command(BaseCommand):

    help = u"Замена типа у локации"
    requires_model_validation = True

    step_limit = 200

    def handle(self, *args, **options):
        main_time = time()
        print u"Start replace type...."

        count_locations = Locations.objects.count()
        for index, offset in enumerate(xrange(0, count_locations, self.step_limit), start=1):
            start = time()

            try:
                self.replace_type_chunk(offset)
            except Exception, e:
                self.print_error(e)

            print u"Elapsed time: {0}, Chunk: {1}".format(time() - start, index * self.step_limit)

        print u"Total Elapsed time: {0}".format(time() - main_time)


    @transaction.commit_on_success
    def replace_type_chunk(self, offset):
        o_loc = Locations.objects.order_by('id')[offset:offset + self.step_limit]
        t = dict(APP_CONTENTS_LOC_TYPE)

        for item in o_loc:
            pattern = urlparse.urlsplit(item.url_view).netloc

            for i in t.keys():
                if i in pattern:
                    item.type = i
                    item.save()

                    break


    def print_error(self, e):
        exc_type, exc_value, exc_traceback = sys.exc_info()
        trace_msg = u''.join(traceback.format_tb(exc_traceback))

        error_msg = u"=============================\n"
        error_msg += u"Error: %s\n" % e
        error_msg += u"=============================\n"
        error_msg += u"Traceback:\n%s\n" % trace_msg
        error_msg += u"=============================\n"

        print error_msg
