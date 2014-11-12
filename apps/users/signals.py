# coding: utf-8

import json

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.users.tasks import notification
from apps.users.models import User, UsersProfile, Feed
from apps.users.constants import FILM_O, PERSON_O

from rest_framework.authtoken.models import Token


@receiver(post_save, sender=get_user_model())
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=User)
def add_profile_to_user(instance, **kwargs):
    profile, flag = UsersProfile.objects.get_or_create(user=instance)


@receiver(post_save, sender=Feed)
def add_feed(instance, created, **kwargs):
    if created:
        if instance.type in (PERSON_O, FILM_O,):
            try:
                data = json.loads(instance.object)
                if instance.type == PERSON_O:
                    id_ = data['film']['id']
                else:
                    id_ = data['id']

                kw = {'id_': id_, 'type_': instance.type}
                notification.apply_async(kwargs=kw)
            except Exception, e:
                pass
