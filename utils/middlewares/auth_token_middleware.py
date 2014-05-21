# coding: utf-8
from apps.users.backends import CookiesSessionAuthentication


class AuthTokenMiddleware(object):

    def process_request(self, request):
        request.user = CookiesSessionAuthentication().authenticate(request)

