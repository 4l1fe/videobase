# coding: utf-8
from django.contrib.auth.models import AnonymousUser

from tocken_session_backend import SessionTokenAuthentication


class CookiesSessionAuthentication(SessionTokenAuthentication):

    def authenticate(self, request):
        if not request.is_ajax() and isinstance(request.user, AnonymousUser):
            token = request.COOKIES.get('x-session', None)
            try:
                return self.authenticate_credentials(token)[0]
            except Exception:
                return AnonymousUser()