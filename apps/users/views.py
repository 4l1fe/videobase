# coding: utf-8
from datetime import datetime, timedelta
from django.shortcuts import render
from django.views.generic import View, TemplateView
from django import forms
from django.forms.extras.widgets import SelectDateWidget
from itertools import groupby

from apps.users.logentry_summary import *
from apps.films.constants import APP_JQUERY_PATH

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
