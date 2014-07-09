from django.core.management.base import BaseCommand
from crawler.person_info import update_person_info
from apps.films.models.persons import Persons


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        pass
        # for i in range(1, 101):
        #     person = Persons.objects.get(id=i)
        #     update_person_info(person)