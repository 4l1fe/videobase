from django.core.management import BaseCommand
from crawler.locrobots.mail_ru.mail_robot import MailRobot


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        MailRobot().get_film_data()
