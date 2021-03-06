# coding: utf-8

from django.db.models.signals import post_save, pre_delete, post_delete
from django.dispatch import receiver

from apps.films.models import Persons, Genres
from utils.common import create_thumbnail, delete_thumbnail, check_callable_function

__all__ = [
    'post_save_handler', 'pre_delete_handler', 'erase_cache_genre_handler'
]

@receiver(post_save, sender=Persons)
def post_save_handler(sender, **kwargs):
    if check_callable_function(kwargs['instance'], 'photo'):
        create_thumbnail(kwargs['instance'].photo.path)


@receiver(pre_delete, sender=Persons)
def pre_delete_handler(sender, **kwargs):
    if check_callable_function(kwargs['instance'], 'photo'):
        delete_thumbnail(kwargs['instance'].photo.path)


@receiver([post_delete, post_save], sender=Genres)
def erase_cache_genre_handler(sender, **kwargs):
    from django.core.cache import cache

    cache.delete(Genres.get_cache_key())
