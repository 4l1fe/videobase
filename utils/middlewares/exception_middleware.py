# coding: utf-8
from social.exceptions import AuthAlreadyAssociated

from django.shortcuts import redirect


class ExceptionMiddleware(object):

    def process_exception(self, response, exception):
        if isinstance(exception, AuthAlreadyAssociated):
            return redirect('profile_view')
