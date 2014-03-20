# coding: utf-8

from django.db.models.signals import post_save, pre_delete

from apps.films.models import Persons
from utils.common import *


def post_save_handler(sender, **kwargs):
    if check_callable_function( kwargs['instance'], 'photo'):
        create_thumbnail(kwargs['instance'].photo.path)

post_save.connect(post_save_handler, sender=Persons)


def pre_delete_handler(sender, **kwargs):
    if check_callable_function( kwargs['instance'], 'photo'):
        delete_thumbnail(kwargs['instance'].photo.path)

pre_delete.connect(pre_delete_handler, sender=Persons)
