# coding: utf-8
from apps.users.models.api_session import SessionToken, UsersApiSessions


def create_new_session(user):

    token = SessionToken(user=user)

    token.save()

    session = UsersApiSessions(token=token)

    session.save()

    return session
