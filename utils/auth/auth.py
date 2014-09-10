# coding: utf-8
from videobase import settings

from django.contrib.auth import load_backend
from django.core.exceptions import ImproperlyConfigured


def get_template_backends():
    backends = []
    for backend_path in settings.TEMPLATE_AUTHENTICATION_BACKENDS:
        backends.append(load_backend(backend_path))
    if not backends:
        raise ImproperlyConfigured('No authentication backends have been defined. Does AUTHENTICATION_BACKENDS contain anything?')
    return backends


def authenticate(**credentials):
    """
    If the given credentials are valid, return a User object.
    """
    for backend in get_template_backends():
        try:
            user, session = backend.authenticate(**credentials)
        except TypeError:
            # This backend doesn't accept these credentials as arguments. Try the next one.
            continue
        if user is None:
            continue
        # Annotate the user object with the path of the backend.
        user.backend = "%s.%s" % (backend.__module__, backend.__class__.__name__)
        return user, session

    return None, None