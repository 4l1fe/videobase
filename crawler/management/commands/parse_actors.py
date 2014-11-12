# coding: utf-8
from django.core.management.base import NoArgsCommand
from crawler.datarobots.kinopoisk_ru.parse_actors import PersoneParser


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        page_dump = PersoneParser.acquire_page(301, True)
        PersoneParser.update_persons_films_with_indexes(page_dump,301)
        print page_dump





