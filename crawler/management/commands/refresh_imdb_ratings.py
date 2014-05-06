# coding: utf-8

from django.core.management.base import NoArgsCommand

from crawler.imdbratings import process_all
import  logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class Command(NoArgsCommand):

    help = u'Обновить IMDB рейтинг'
    requires_model_validation = True

    def handle_noargs(self, **options):
        process_all()



