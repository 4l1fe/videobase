# coding: utf-8
import datetime

from django.contrib.auth.models import AnonymousUser

from auth import authenticate


def auth_user(func):
    def wrapper(request, *args, **kwargs):
        if isinstance(request.user, AnonymousUser):
            x_session = request.COOKIES.get('x-session', None)
            x_token = request.COOKIES.get('x-token', None)
            user, session = authenticate(x_session=x_session, x_token=x_token, request=request)
            if user is None:
                user = AnonymousUser()
            request.user = user
            response = func(request, *args, **kwargs)
            if session:
                #Two weeks
                max_age = 30 * 24 * 60 * 60
                expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
                response.set_cookie('x-session', session, max_age=max_age, expires=expires)
        else:
            response = func(request, *args, **kwargs)

        return response
    return wrapper

