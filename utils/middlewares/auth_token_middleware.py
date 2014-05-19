# coding: utf-8
from django.contrib.auth.models import AnonymousUser

from apps.users.models import SessionToken


class AuthTokenMiddleware(object):

    def process_request(self, request):
        token = request.COOKIES.get('x-session', None)
        if isinstance(request.user, AnonymousUser):
            try:
                user = SessionToken.objects.get(key=token).user
                if user.is_active:
                    request.user =user
                else:
                    request.user = AnonymousUser()
            except Exception:
                request.user = AnonymousUser()

