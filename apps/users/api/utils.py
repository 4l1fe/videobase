# coding: utf-8

from django.db import transaction
from apps.users.models.api_session import SessionToken, UsersApiSessions


@transaction.commit_on_success()
def create_new_session(user):
    token = SessionToken(user=user)
    token.save()

    session = UsersApiSessions(token=token)
    session.save()

    return session
