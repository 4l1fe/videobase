# coding: utf-8

from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.users.models import User, UsersProfile, Feed


@receiver(post_save, sender=User)
def add_profile_to_user(instance, **kwargs):
    profile, flag = UsersProfile.objects.get_or_create(user=instance)
    profile.save()


@receiver(post_save, sender=Feed)
def notification(instance, **kwargs):
    profile, flag = UsersProfile.objects.get_or_create(user=instance)
    profile.save()