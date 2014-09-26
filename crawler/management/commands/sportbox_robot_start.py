from django.core.management import BaseCommand
from crawler.locrobots.mail_ru.mail_robot import MailRobot
from crawler.translation_robot.ntvplus_ru.parse import parse_translation


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        MailRobot().get_film_data()
