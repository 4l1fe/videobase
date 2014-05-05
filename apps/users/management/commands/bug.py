from apps.robots.models import Robots
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.users.api.users import vbUser


class Command(BaseCommand):

    def handle(self,*args,**kwargs):
        user = User.objects.get_or_create(username='user3')
        vbu = vbUser(user)

        print vbu.data



