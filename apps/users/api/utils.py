# coding: utf-8
from django.db import transaction

from apps.users.models import SessionToken


@transaction.commit_on_success()
def create_new_session(user):
    session = SessionToken(user=user)
    session.save()
    return session
