# coding: utf-8
from django.views.generic import base
from django.utils.decorators import method_decorator

from decorators import auth_user


class View(base.View):

    @method_decorator(auth_user)
    def dispatch(self, request, *args, **kwargs):
        return super(View, self).dispatch(request, *args, **kwargs)

