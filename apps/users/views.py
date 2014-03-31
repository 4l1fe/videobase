# coding: utf-8
from datetime import datetime, timedelta
from django.shortcuts import render
from django.views.generic import View, TemplateView
from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from itertools import groupby
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import login
from registration import signals
import warnings

from registration.backends.simple.views import RegistrationView as BaseRegistrationView
from apps.users.logentry_summary import *
from apps.films.constants import APP_JQUERY_PATH
from apps.users.models import Users

class RegistrationView(BaseRegistrationView):
    """
    A registration backend which implements the simplest possible
    workflow: a user supplies a username, email address and password
    (the bare minimum for a useful account), and is immediately signed
    up and logged in).

    """
    def register(self, request, **cleaned_data):
        email, password = cleaned_data['email'], cleaned_data['password1']
        extra_params = {}

        if cleaned_data.get('firstname'):
            extra_params['firstname'] = cleaned_data.get('firstname')

        if cleaned_data.get('lastname'):
            extra_params['lastname'] = cleaned_data.get('lastname')

        try:
            if Users.objects.get(is_admin=True):
                extra_params['is_admin'] = False
        except:
            warnings.warn("== CREATE ADMIN USER =========: email - {0}".format(email), Warning )
            extra_params['is_admin'] = True

        Users.objects.create_user(email, password, **extra_params)

        new_user = authenticate(username=email, password=password)
        login(request, new_user)
        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=request)
        return new_user

    def get_success_url(self, request, user):
        if user.is_admin:
            return ('/admin/', (), {})
        else:
            return ('/accounts/profile/', (), {})

class FilterForm(forms.Form):
    start_at = forms.DateField(widget=SelectDateWidget(), label=u'с')
    end_at = forms.DateField(widget=SelectDateWidget(), label=u'по')

class LogentrySummaryView(TemplateView):
    template_name = 'admin/logentry_summary.html'

    def get_context_data(self, **kwargs):

        context = super( LogentrySummaryView, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            filter_form = FilterForm(self.request.POST)
            end_at = filter_form['end_at'].value()
            start_at = filter_form['start_at'].value()
            report = LogentrySummary(period ={'start_at': start_at, 'end_at': end_at})
        else:
            end_at = datetime.now()
            end_at = end_at.replace(hour=23, minute=59, second=59, microsecond=59)
            start_at = (datetime.now() - timedelta(days = datetime.now().weekday()))
            start_at = start_at.replace(hour=0, minute=0, second=0, microsecond=0)
            report = LogentrySummary(period ={'start_at': start_at, 'end_at': end_at})
            filter_form = FilterForm(initial={ 'end_at': end_at, 'start_at': start_at})

        context['jquery_path'] = APP_JQUERY_PATH
        context['report_data'] = report.summary()
        context['filter_form'] = filter_form.as_table()

        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        return self.render_to_response(context)

class UserAccountView(TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super(UserAccountView, self).get_context_data(**kwargs)
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserAccountView, self).dispatch(*args, **kwargs)
