# coding: utf-8
from django.contrib.auth.models import AnonymousUser

from apps.users.models import SessionToken


class AuthTokenMiddleware(object):

    def process_request(self, request):
        token = request.COOKIES.get('x-session', None)
        try:
            request.user = SessionToken.objects.get(key=token).user
        except Exception:
            request.user = AnonymousUser()

