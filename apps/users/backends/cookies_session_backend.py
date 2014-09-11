# coding: utf-8
import datetime

from django.utils import timezone
from rest_framework.authtoken.models import Token

from apps.users.models import SessionToken
from videobase import settings


class CookiesSessionAuthentication(object):

    model = SessionToken

    def authenticate(self, x_session, **kwargs):
        session = None
        try:
            token = self.model.objects.get(key=x_session)
        except self.model.DoesNotExist:
            return None, None
        user = token.user
        if timezone.now() - token.updated >= datetime.timedelta(minutes=settings.API_SESSION_EXPIRATION_TIME):
            token.is_active = False
            token.save()
            new_token = self.model(user=user)
            new_token.save()
            session = new_token
        elif not token.is_active:
            return None, None
        else:
            token.updated = timezone.now()
            token.save()
        return user, session


class CookiesTokenAuthentication(object):
    model = Token

    def authenticate(self, x_token, request, **kwargs):
        try:
            token = self.model.objects.get(key=x_token)
        except self.model.DoesNotExist:
            return None, None
        user = token.user
        new_token = SessionToken(user=user)
        new_token.save()
        session = new_token
        return user, session
