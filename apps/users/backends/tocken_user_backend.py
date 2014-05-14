# coding: utf-8
from rest_framework import exceptions
from rest_framework.authtoken.models import Token

from tocken_session_backend import SessionTokenAuthentication

from videobase import settings


class UserTokenAuthentication(SessionTokenAuthentication):

    model = Token
    token = settings.STANDART_HTTP_USER_TOKEN_HEADER

    def authenticate_credentials(self, key):
        try:
            token = self.model.objects.get(key=key)
        except self.model.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted')

        return token.user, token

    def authenticate_header(self, request):
        return settings.HTTP_USER_TOKEN_TYPE
