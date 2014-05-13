# coding: utf-8
from django.utils import timezone

from rest_framework import HTTP_HEADER_ENCODING
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions

from apps.users.models import SessionToken, UsersApiSessions


from videobase import settings


class SessionTokenAuthentication(BaseAuthentication):
    """
    A custom token model may be used, but must have the following properties.

    * key -- The string identifying the token
    * user -- The user to which the token belongs
    """

    model = SessionToken
    token = settings.STANDART_HTTP_SESSION_TOKEN_HEADER

    def authenticate(self, request):
        try:
            auth = request.META[self.token]
            if isinstance(auth, list) and len(auth) > 2:
                msg = 'Invalid token header. Token string should not contain spaces.'
                raise exceptions.AuthenticationFailed(msg)
            if auth == b'':
                msg = 'Invalid token header. No credentials provided.'
                raise exceptions.AuthenticationFailed(msg)
            else:
                if type(auth) == type(b''):
                    auth = auth.encode(HTTP_HEADER_ENCODING)
        except KeyError:
            return None

        return self.authenticate_credentials(auth)

    def authenticate_credentials(self, key):
        try:
            token = self.model.objects.get(key=key)
        except self.model.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted')

        try:
            uas = UsersApiSessions.objects.get(token=token)

            if uas.get_expiration_time() < timezone.now():
                raise exceptions.AuthenticationFailed('Session expired')
            if not uas.active:
                raise exceptions.AuthenticationFailed('Session not active')

        except UsersApiSessions.DoesNotExist:
            raise exceptions.AuthenticationFailed('There is no session associated with this token')

        return token.user, token

    def authenticate_header(self, request):
        return settings.HTTP_SESSION_TOKEN_TYPE