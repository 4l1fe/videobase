# coding: utf-8
import datetime

from django.utils import timezone
from django.contrib.auth.models import AnonymousUser
from django.core.urlresolvers import resolve

from rest_framework.authtoken.models import Token

from videobase import settings
from apps.users.models import SessionToken


def auth(x_token=None, x_session=None):
    user = AnonymousUser()
    token = None
    is_new = False
    if not x_session is None and not x_token is None:
        try:
            user_token = Token.objects.get(key=x_token)
            sess_token = SessionToken.objects.get(key=x_session)
        except (SessionToken.DoesNotExist, Token.DoesNotExist):
            return user, token, is_new
        if not sess_token.is_active or sess_token.user != user_token.user:
            # Token not active
            # Or user_token and token_session for user not equal
            return user, token, is_new
        elif timezone.now() - sess_token.updated >= settings.SESSION_EXPIRATION_TIME:
            # Token is valid but is expired
            sess_token.is_active = False
            sess_token.save()
            new_token = SessionToken(user=sess_token.user)
            new_token.save()
            # Return values
            token = new_token
            is_new = True
            user = new_token.user
        else:
            # Token is not expired and is valid
            sess_token.updated = timezone.now()
            sess_token.save()
            # Return values
            token = sess_token
            is_new = False
            user = sess_token.user
    return user, token, is_new


class AuthenticationMiddleware(object):
    def __init__(self):
        self.api_namespaces = ['films_api', 'users_api', 'casts_api']
        self.session = None

    def process_request(self, request):
        self.session = None
        # Not API request
        if resolve(request.path).namespace not in self.api_namespaces:
            if isinstance(request.user, AnonymousUser):
                # Check user
                x_session = request.COOKIES.get('x-session', None)
                x_token = request.COOKIES.get('x-token', None)
                # Get user or None
                request.user, token, is_new = auth(x_session=x_session, x_token=x_token)
                if not token is None and is_new:
                    self.session = token

    def process_response(self, request, response):
        if not self.session is None:
            max_age = 30 * 24 * 60 * 60
            expires = datetime.datetime.strftime(timezone.now() + settings.SESSION_EXPIRATION_TIME, "%a, %d-%b-%Y %H:%M:%S GMT")
            response.set_cookie('x-session', self.session.key, max_age=max_age, expires=expires)

        return response