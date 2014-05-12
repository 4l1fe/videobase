# coding: utf-8

from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from apps.films.models import Persons
from utils.common import create_thumbnail, delete_thumbnail, check_callable_function


@receiver(post_save, sender=Persons)
def post_save_handler(sender, **kwargs):
    if check_callable_function(kwargs['instance'], 'photo'):
        create_thumbnail(kwargs['instance'].photo.path)


@receiver(pre_delete, sender=Persons)
def pre_delete_handler(sender, **kwargs):
    if check_callable_function(kwargs['instance'], 'photo'):
        delete_thumbnail(kwargs['instance'].photo.path)
